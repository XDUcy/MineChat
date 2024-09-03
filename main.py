import re
import time
import json
from database.vectordb import vectordb
from source.LLM import Yuan2B
from source.LLM_api import GLM4Flash
from mcrcon import MCRcon
import asyncio

class Asistant:
    def __init__(self, log_path:str, llm, vectordb:vectordb, prompt_template:str, server:str, password:str, local = False):
        print("Listener initialized.. Log path:" + log_path)
        self.log_path = log_path
        self.last_modified_time = 0
        self.fp = None
        if local:
            self.llm = Yuan2B(llm)
        else:
            self.llm = GLM4Flash(llm)
        self.vectordb = vectordb
        self.queue = asyncio.Queue()
        self.prompt_template = prompt_template
        self.rcon = MCRcon(server, password, port=25575)
        try:
            self.fp = open(log_path, "r", encoding="gb2312", errors='ignore') # mc server log编码为gb2312
            self.fp.seek(0, 2)  # 文件指针移到末尾
        except FileNotFoundError:
            print("log file not found")
        self.rcon.connect()

    def _connect(self, ip, password):
        return MCRcon(ip, password)

    async def listen(self):
        # listen调试方法，手动复制一行玩家信息即可，相当于新增消息
        if self.fp is None:
            print("Log file is not open.")
            return
        while True:
            line = self.fp.readline()
            if not line:
                await asyncio.sleep(1)
            else:
                line.replace("\r\n", "\n")
                if res := re.search(": <(.+)>(.+)", line):
                    # 正则匹配出的格式： res.group1 玩家名, res.group2 内容
                    username = res.group(1)
                    content = res.group(2)
                    msg_dict = {'user':username, 'content':content}
                    await self.queue.put(msg_dict)
                    print(f"{username}'s message {content} enqueued.")

    async def process(self):
        while True:
            msg_dict = await self.queue.get()
            context = ""
            docs = self.vectordb.client.similarity_search(query=msg_dict['content'], k=5)
            for i, doc in enumerate(docs):
                context += "Context {}: {}\n".format(i, doc.page_content.replace('\n', ''))
            response = self.llm(prompt=self.prompt_template.format(context=context, question=msg_dict['content']))
            print(
                self.prompt_template.format(
                    context=context, question=msg_dict["content"]
                )
            )
            print("----\n", response)
            resp = self.rcon.command(f"/say {response}")

async def MineChat(assistant):
    await asyncio.gather(assistant.listen(), assistant.process())


prompt_template = """你是一个嵌入在Minecraft游戏中的智能助手，名叫MineChat，\\
    你的任务是帮助玩家使用游戏指令改善游戏体验，请你不要输出任何markdown格式内容，根据玩家要求输出命令或简单回答即可。不要生成任何与编程相关的内容！
    请记住，MineChat就是你，你就是MineChat，是一个Minecraft游戏内置助手。
    上下文：{context}
    问题：{question}
"""
db = vectordb("MineChat")
db.scan()
cfg = json.load(open("config.json", "r", encoding='utf8'))
log_path = cfg.get("log_path")
llm_dir = cfg.get("llm_dir")
embed_model = cfg.get("embed_model")
zhipu_token = cfg.get("zhipu_token")
local = cfg.get("local")

if local:
    llm = llm_dir
else:
    llm = zhipu_token

minechat = Asistant(log_path=log_path, llm=llm, vectordb=db, prompt_template=prompt_template, server='127.0.0.1', password='123456')
asyncio.run(MineChat(minechat))