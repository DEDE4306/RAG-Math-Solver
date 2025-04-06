# vector_store.py
import faiss
import os
import numpy as np
import pickle

class VectorStore:
    def __init__(self, dim, index_path="faiss_index.index", meta_path="metadata.pkl"):
        self.index_path = index_path
        self.meta_path = meta_path
        self.index = faiss.IndexFlatL2(dim)  # 用于基本 L2 相似度检索
        self.metadata = []

        if os.path.exists(index_path) and os.path.exists(meta_path):
            self.load()

    def add(self, vectors, metas):
        self.index.add(vectors)
        self.metadata.extend(metas)

    def search(self, query_vector, top_k=5):
        D, I = self.index.search(query_vector, top_k)
        results = []
        for idx in I[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])
        return results

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, 'wb') as f:
            pickle.dump(self.metadata, f)

    def load(self):
        self.index = faiss.read_index(self.index_path)
        with open(self.meta_path, 'rb') as f:
            self.metadata = pickle.load(f)