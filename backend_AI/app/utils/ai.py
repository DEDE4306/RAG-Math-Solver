# services/llm.py
from ..llm.qwen_client import QwenClient
from ..rag.embedder import Embedder
from ..rag.faiss_indexer import FaissIndexer
from config import api_key
from pathlib import Path
from typing import List, Dict

def chat_completion(messages: List[Dict], top_k: int = 5) -> str:
    """
    输入问题，自动完成向量化、检索、构造 Prompt 和模型调用，返回回答
    """
    # 提取最新一条 user 消息作为查询
    question = next((m["content"] for m in reversed(messages) if m["role"] == "user"), None)
    if question is None:
        return "无用户提问内容"
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

    # 构造系统提示
    system_prompt = {
        "role": "system",
        "content": "你是一个精通数学的 AI，现在需要你为同学或老师解决小学到高中的数学问题。"
    }

    # 插入 context 到最后一条 user 提问中
    updated_messages = []
    for m in messages:
        if m == messages[-1] and m["role"] == "user":
            # 插入 context 到最后问题里
            m = {
                "role": "user",
                "content": f"{m['content']}\n\n以下是一些相关的数学知识片段：\n{context}"
            }
        updated_messages.append(m)

    full_messages = [system_prompt] + updated_messages
    print("==== Prompt 发送 ====")
    for msg in full_messages:
        print(f"[{msg['role']}] {msg['content']}\n")

    # 调用模型
    qwen_client = QwenClient(api_key=api_key)
    result = qwen_client.chat(full_messages)
    return result