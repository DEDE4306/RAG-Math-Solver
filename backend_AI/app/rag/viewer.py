# viewer.py
from faiss_indexer import FaissIndexer

# 创建 indexer 并加载
indexer = FaissIndexer(index_path='../vector/numina.index', texts_path='../vector/numina.pkl')
indexer.load()

# 查看前几个文本和向量
print("文本示例：")
for i in range(3):
    print(f"{i+1}: {indexer.texts[i]}")

print("\n 向量示例（第1个）：")
print(indexer.index.reconstruct(0))