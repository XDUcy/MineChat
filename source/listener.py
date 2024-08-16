import time
import os
from mcrcon import MCRcon
import re


class Listener:
    def __init__(self, log_path):
        print("Listener initialized.. Log path:" + log_path)
        self.log_path = log_path
        self.last_modified_time = 0
        self.fp = None
        try:
            self.fp = open(log_path, 'r', encoding="utf8")
            self.fp.seek(0, 2) # 文件指针移到末尾
        except FileNotFoundError:
            print("log file not found")

    def listen(self):
        # listen调试方法，手动复制一行玩家信息即可，相当于新增消息
        if self.fp is None:
            print('Log file is not open.')
            return
        while True:
            line = self.fp.readline()
            if not line:
                time.sleep(1)
            else:
                line.replace('\r\n', '\n')
                if res := re.search(": <(.+)>(.+)", line):
                    # 正则匹配出的格式： res.group1 玩家名, res.group2 内容
                    msg = res.group(2)  # 暂时忽略玩家名
                    print("我已经接收到了玩家信息，这将要给大模型来完成对话或者其他处理", msg)


log_path = './logs/latest.log'
listener = Listener(log_path)
listener.listen()

"""
先不考虑Remote Control使用
with MCRcon("127.0.0.1", "123456") as mcr:
    resp = mcr.command("/list")
    print("测试RCON远程命令返回", resp)
    mcr.command("/time set day")
"""
