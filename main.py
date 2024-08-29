from source.LLM import Yuan2B
from source.embedding import EmbeddingModel
from langchain_community.document_loaders import PyPDFLoader
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from database.DataUtils import vectordb

prompt = """你是一个嵌入在Minecraft游戏中的智能助手，名叫MineChat，\\
    你的任务是帮助玩家在游戏中解答各种问题。你的回答要简洁、准确，并且与游戏内的规则和内容相关联。\\
    请你根据玩家问题以及以下上下文来回答最后的问题。
    上下文：{context}
    问题：{question}
"""

db = vectordb("MineChat")
db.scan()
print("Vectordb loaded, current knowledge:\n", db.log_data["knowledge_list"])

results = db.client.similarity_search("Tell me more about Redstone?", k=5)
for i, doc in enumerate(results):
    print(f"({i}):", doc.page_content.replace('\n', ''))
