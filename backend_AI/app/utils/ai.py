# services/llm.py
from ..llm.qwen_client import QwenClient
from ..rag.embedder import Embedder
from ..rag.faiss_indexer import FaissIndexer
from config import api_key
from pathlib import Path

def chat_completion(question: str, top_k: int = 5) -> str:
    """
    输入问题，自动完成向量化、检索、构造 Prompt 和模型调用，返回回答
    """
    # 向量化用户提问
    embedder = Embedder(model_name="BAAI/bge-large-zh-v1.5")
    query_vector = embedder.embed(question)

    # 获取向量化数据
    vector_dir = Path(__file__).parent.parent / "vector"  # vector 在项目根目录下
    # print(vector_dir)
    index_path = str(vector_dir / "formula.index")
    texts_path = str(vector_dir / "formula.pkl")
    indexer = FaissIndexer(index_path=index_path, texts_path=texts_path)
    indexer.load()

    # 检索 top-k 上下文
    retrieved_texts_and_scores = indexer.search(query_vector, k=top_k)
    context = "\n".join([f"- {text}" for text, _ in retrieved_texts_and_scores])

    # 构造提示词（Prompt）
    prompt = f"请回答问题：\n{question}\n\n以下是一些相关的数学知识片段：\n{context}"
    print(prompt)

    # if len(prompt) > 3072:
    #     prompt = prompt[:3072]
    # print("prompt 过长，进行截断")

    # 调用模型
    qwen_client = QwenClient(api_key=api_key)
    result = qwen_client.chat(prompt)
    return result