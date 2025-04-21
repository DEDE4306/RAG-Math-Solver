# viewer.py
import faiss
import pickle
import numpy as np
from embedder import Embedder

# 初始化 embedder（使用 GPU）
embedder = Embedder()

# 读取 FAISS 索引
index = faiss.read_index("try.index")

# 读取对应文本
with open("try_texts.pkl", "rb") as f:
    texts = pickle.load(f)

# 打印基本信息
print(f"Index total vectors: {index.ntotal}")
print(f"Loaded {len(texts)} texts.")

# 输出所有向量及对应文本
for i in range(index.ntotal):
    vector = index.reconstruct(i)  # 获取第 i 个向量
    text = texts[i]

    print(f"\n🔢 Index {i}")
    print(f"Text: {text}")
    print(f"ector (dim={len(vector)}): {vector[:10]}...")  # 只显示前10维，太长会刷屏