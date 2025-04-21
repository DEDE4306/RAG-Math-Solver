from embedder import Embedder

# 初始化嵌入器
embedder = Embedder()

# 测试数据
texts = [
    "The Pythagorean theorem: a^2 + b^2 = c^2",
    "Newton's second law: F = ma"
]

# 获取向量
embeddings = embedder.embed(texts)

# 打印向量维度和部分内容
print(f"Shape: {embeddings.shape}")
print("First vector (truncated):", embeddings[0][:5])