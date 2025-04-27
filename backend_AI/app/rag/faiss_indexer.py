import faiss
import numpy as np
import os
import pickle


class FaissIndexer:
    def __init__(self, dim=None, index_path='faiss.index', texts_path='texts.pkl'):
        """

        :param dim: 向量维度
        :param index_path: FAISS index 保存路径
        :param texts_path: 对应文本保存路径
        """
        self.index_path = index_path
        self.texts_path = texts_path
        self.texts = []                          # 存储原始文本的列表
        if dim is not None:
            self.index = faiss.IndexFlatL2(dim)
        else:
            self.index = None  # 先不初始化，等加载或 build 再处理

    def add(self, vectors, texts):
        if self.index is None:
            dim = vectors.shape[1]
            self.index = faiss.IndexFlatL2(dim)
        else:
            assert self.index.d == vectors.shape[1], \
                f"向量维度不一致！已有索引维度是 {self.index.d}，现在传入的是 {vectors.shape[1]}"
        self.index.add(np.array(vectors).astype('float32'))  # 将向量加入索引（确保类型为 float32）
        self.texts.extend(texts)                              # 同步添加对应文本

    def save(self):
        faiss.write_index(self.index, self.index_path)        # 保存 FAISS 索引到文件
        with open(self.texts_path, 'wb') as f:                # 保存文本数据（用 pickle）
            pickle.dump(self.texts, f)
        print(f"index saved:{self.index_path}")
        print(f"texts saved:{self.texts_path}")

    def load(self):
        # 加载索引文件和文本文件
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
        if os.path.exists(self.texts_path):
            with open(self.texts_path, 'rb') as f:
                self.texts = pickle.load(f)

    def search(self, query_vector, k=5):
        if self.index is None:
            raise ValueError("Index not loaded or built")
        D, I = self.index.search(query_vector.astype('float32'), k)  # 对查询向量执行相似度搜索
        return [(self.texts[i], D[0][idx]) for idx, i in enumerate(I[0])]  # 返回前 k 个文本及其距离

    def build_from_dataset(self, dataset_embedder):
        """

        :param dataset_embedder: 从 dataset_embedder 加载文本并建立索引
        :return:
        """
        embeddings, texts = dataset_embedder.get_embeddings()
        self.add(embeddings, texts)

