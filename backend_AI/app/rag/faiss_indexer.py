import faiss
import numpy as np
import os
import pickle

class FaissIndexer:
    def __init__(self, dim, index_path='faiss.index', texts_path='texts.pkl'):
        """

        :param dim:
        :param index_path: FAISS index 保存路径
        :param texts_path: 对应文本保存路径
        """
        self.index_path = index_path
        self.texts_path = texts_path
        self.index = faiss.IndexFlatL2(dim)      # 初始化 FAISS 索引，使用 L2 距离
        self.texts = []                          # 存储原始文本的列表

    def add(self, vectors, texts):
        self.index.add(np.array(vectors).astype('float32'))  # 将向量加入索引（确保类型为 float32）
        self.texts.extend(texts)                              # 同步添加对应文本

    def save(self):
        faiss.write_index(self.index, self.index_path)        # 保存 FAISS 索引到文件
        with open(self.texts_path, 'wb') as f:                # 保存文本数据（用 pickle）
            pickle.dump(self.texts, f)

    def load(self):
        if os.path.exists(self.index_path):                   # 如果索引文件存在
            self.index = faiss.read_index(self.index_path)    # 加载索引
        if os.path.exists(self.texts_path):                   # 如果文本文件存在
            with open(self.texts_path, 'rb') as f:
                self.texts = pickle.load(f)                   # 加载文本内容

    def search(self, query_vector, k=5):
        D, I = self.index.search(query_vector.astype('float32'), k)  # 对查询向量执行相似度搜索
        return [(self.texts[i], D[0][idx]) for idx, i in enumerate(I[0])]  # 返回前 k 个文本及其距离