# 暂时不用

from tqdm import tqdm
from typing import List
import os
import json
import numpy as np


class VectorDB:

    def __init__(self, docs: List = []) -> None:
        self.docs = docs

    def get_vector(self, EmbeddingModel):
        self.vectors = []
        for doc in tqdm(self.docs):
            self.vectors.append(EmbeddingModel.get_embedding(doc))
        return self.vectors

    def export_data(self, data_path="db"):
        try:
            if not os.path.exists(data_path):
                os.makedirs(data_path)
            with open(f"{data_path}/doecment.json", "w", encoding="utf-8") as f:
                json.dump(self.docs, f, ensure_ascii=False)
            with open(f"{data_path}/vectors.json", "w", encoding="utf-8") as f:
                json.dump(self.vectors, f)
        except Exception:
            return False
        return True

    # 加载json文件中的向量和字块，得到向量列表、字块列表,默认路径为'database'
    def load_vector(self, path: str = "db") -> None:
        with open(f"{path}/vectors.json", "r", encoding="utf-8") as f:
            self.vectors = json.load(f)
        with open(f"{path}/doecment.json", "r", encoding="utf-8") as f:
            self.document = json.load(f)
        # 求向量的余弦相似度，传入两个向量和一个embedding模型，返回一个相似度

    def get_similarity(
        self, vector1: List[float], vector2: List[float], embedding_model
    ) -> float:
        return embedding_model.compare_v(vector1, vector2)

    # 求一个字符串和向量列表里的所有向量的相似度，表进行排序，返回相似度前k个的子块列表
    def query(self, query: str, EmbeddingModel, k: int = 1) -> List[str]:
        query_vector = EmbeddingModel.get_embedding(query)
        result = np.array(
            [
                self.get_similarity(query_vector, vector, EmbeddingModel)
                for vector in self.vectors
            ]
        )
        return np.array(self.document)[result.argsort()[-k:][::-1]].tolist()
