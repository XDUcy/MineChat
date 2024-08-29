import os
import json
from datetime import datetime
from source.embedding import EmbeddingModel
from langchain_community.document_loaders import PyPDFLoader
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain_chroma import Chroma
from chromadb.utils import embedding_functions

# 维护向量知识库
# 1. 一个Chroma对象 + 已向量化内容列表（json）
# 2. 功能：
#   (1)扫描./dataset文件夹，检查未更新的知识可选添加
#   (2)向量化知识，用于RAG
#   (3)向量检索内容

class vectordb:
    def __init__(self, name, root_path='./database/'):
        self.name = name
        self.path = os.path.join(root_path, name)
        self.log_file = os.path.join(self.path, 'log.txt')
        self.log_data = {
            'knowledge_list':[],
            'last_update':None
        }
        # self.list = []

        if os.path.exists(self.path):
            print(f"Vectordb '{name}' already exists, loading...")
        else:
            print(f"Vectordb '{name}' not exists, creating...")
            os.makedirs(self.path)

        if os.path.exists(self.log_file):
            print(f"Log file already exists, loading...")
            with open(self.log_file, 'r') as log_file:
                self.log_data = json.load(log_file)
        else:
            print(f"Log file not exists, creating...")
            self._update_log_file()

        self.embed = EmbeddingModel("D:/Datasets/Pretrained Models/embed/AI-ModelScope/bge-small-zh-v1___5")
        self.client = Chroma(collection_name=self.name,
                             embedding_function=self.embed,
                             persist_directory=self.path)

    def scan(self, path='./dataset/'):
        # 获取所有pdf文件
        pdfs = [os.path.join(path, pdf) for pdf in os.listdir(path) if pdf]
        new_pdfs = [pdf for pdf in pdfs if pdf not in self.log_data['knowledge_list']]
        if new_pdfs:
            print("Found new knowledge, updating...")
            self._update_db(new_pdfs)
            self.log_data["knowledge_list"].extend(new_pdfs)
            self.log_data["last_update"] = datetime.now().isoformat()
            self._update_log_file()
        else:
            print("No new knowledge found.")

    def _update_db(self, pdfs):
        # 读取pdf文件
        for pdf in pdfs:
            loader = PyPDFLoader(pdf)
            docs = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500, chunk_overlap=150
            )
            splits = text_splitter.split_documents(docs)
            self.client.add_documents(splits)
        print(f"Vectordb '{self.name}' updated.")

    def _update_log_file(self):
        with open(self.log_file, 'w+') as log_file:
            json.dump(self.log_data, log_file, indent=4)

"""
pdf = [
    "./dataset/Minecraft Crafting 70 Top Minecraft Essential Crafting-Techniques Guide Expo (Scotts, Jason) (Z-Library).pdf"
]
docs = []

for file_path in pdf:
    loader = PyPDFLoader(file_path)
    docs.extend(loader.load())

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 150
)
splits = text_splitter.split_documents(docs)
# print(len(splits), splits[2].page_content)

embed = EmbeddingModel("D:/Datasets/Pretrained Models/embed/AI-ModelScope/bge-small-zh-v1___5")
vectordb = Chroma.from_documents(
    splits,
    embedding=embed,
    persist_directory='./database/chroma'
)
vectordb.persist()

print(vectordb._collection.count())


"""
