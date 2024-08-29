import os
import json
from datetime import datetime
from source.embedding import EmbeddingModel
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

# 维护向量知识库 Done
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
        # 获取所有docs
        docs = [os.path.join(path, pdf) for pdf in os.listdir(path) if pdf.endswith('.pdf') or pdf.endswith('.txt')]
        new_docs = [doc for doc in docs if doc not in self.log_data['knowledge_list']]
        if new_docs:
            print("Found new knowledge, updating...")
            self.add_pdf(pdfs=[doc for doc in new_docs if doc.endswith('.pdf')])
            self.add_txt(txts=[doc for doc in new_docs if doc.endswith('.txt')])
            self.log_data["knowledge_list"].extend(new_docs)
            self.log_data["last_update"] = datetime.now().isoformat()
            self._update_log_file()
        else:
            print("No new knowledge[pdf] found.")

    def add_txt(self, txts):
        # 读取txt文件
        for txt in txts:
            loader = TextLoader(txt, encoding='UTF-8')
            text = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(separators=['\n', '\n\n'])
            splits = text_splitter.split_documents(text)
            self.client.add_documents(splits)


    def add_pdf(self, pdfs):
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
