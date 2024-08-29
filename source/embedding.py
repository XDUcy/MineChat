from typing import List
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings

class EmbeddingModel(Embeddings):
    def __init__(self, model_name: str):
        self.model = SentenceTransformer("D:/Datasets/Pretrained Models/embed/AI-ModelScope/bge-small-zh-v1___5")
    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        return [self.model.encode(d).tolist() for d in documents]
    def embed_query(self, query: str) -> List[float]:
        return self.model.encode([query])[0].tolist()

if __name__ == "__main__":
    embed = EmbeddingModel("D:/Datasets/Pretrained Models/embed/AI-ModelScope/bge-small-zh-v1___5")
    print(len(embed.embed_query("你好")))