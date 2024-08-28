import os
from source.LLM import Yuan2B
from source.embedding import EmbeddingModel
from langchain_community.document_loaders import PyPDFLoader
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain_chroma import Chroma

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
        # self.list = []

        if os.path.exists(self.path):
            print(f"Vectordb '{name}' already exists, loading...")
        else:
            print(f"Vectordb '{name}' not exists, creating...")

        self.client = Chroma(collection_name=self.name,
                             embedding_function=EmbeddingModel.embed_documents,
                             persist_directory=self.path)
        
    def scan(self, path='./dataset/'):
        # 获取所有pdf文件
        pdfs = [os.path.join(path, pdf) for pdf in os.listdir(path) if pdf]

    def update_db(self, pdfs):
        # 读取pdf文件
        for pdf in pdfs:
            loader = PyPDFLoader(pdf)
            docs = loader.load()
            self.list.extend(docs)
        # 向量化
        self.client.add_documents(self.list)
        print(f"Vectordb '{self.name}' updated.")

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
