# api/send_message.py
from datetime import datetime
from flask import Blueprint,request,jsonify
from ..rag.embedder import Embedder
from ..rag.faiss_indexer import FaissIndexer
from ..models.qwen_client import QwenClient
from pathlib import Path
from dotenv import load_dotenv
import os

chat_bp = Blueprint('chat',__name__,url_prefix='/api/chat') # 创建一个聊天蓝图

@chat_bp.route('/sendMessage',methods=['POST'])
def send_message():
    # try:
        # 获取数据
        data = request.get_json()
        user_question = data.get('content')

        # 向量化用户提问
        embedder = Embedder(model_name="BAAI/bge-large-zh-v1.5")
        query_vector = embedder.embed(user_question)

        # 获取向量化数据
        vector_dir = Path(__file__).parent.parent / "vector"  # vector 在项目根目录下
        print(vector_dir)
        index_path = str(vector_dir / "numina.index")
        texts_path = str(vector_dir / "numina.pkl")
        indexer = FaissIndexer(index_path=index_path, texts_path=texts_path)
        indexer.load()

        # 检索 top-k 上下文
        retrieved_texts_and_scores = indexer.search(query_vector,k=5)
        context = "\n".join([f"- {text}" for text, _ in retrieved_texts_and_scores])

        # 构造提示词（Prompt）
        prompt = f"以下是一些相关的数学知识片段：\n{context}\n\n根据这些信息，请回答问题：\n{user_question}"
        print(prompt)

        # 调用模型
        env_path = Path(__file__).resolve().parents[2] / ".env"
        load_dotenv(dotenv_path=env_path)
        api_key = os.getenv("DASHSCOPE_API_KEY")
        qwen_client = QwenClient(api_key=api_key)
        response_text = qwen_client.chat(prompt)

        # 返回前端
        result = {
            "success": True,
            "msg": "请求成功",
            "response":{
                "messageid":0,
                "role":"assistant",
                "content":response_text,
                "createdat":datetime.now().isoformat()
            }
        }
        return jsonify(result)


    # except Exception as e:
    #     return jsonify({
    #         "success": False,
    #         "msg": f"服务异常：{str(e)}",
    #         "response": {}
    #     })

    # data = request.get_json()
    # user_question = data.get('content')
    # embedder = Embedder(model_name="BAAI/bge-large-zh-v1.5")
    # query_vector = embedder.embed(user_question)
    # # 获取当前文件的绝对路径，再推导出 vector 目录的路径
    # current_dir = Path(__file__).parent  # 当前文件所在目录
    # print(current_dir)
    # vector_dir = current_dir.parent/"vector"  # 假设 vector 在项目根目录下
    # print(vector_dir)
    # index_path = str(vector_dir / "numina.index")
    # texts_path = str(vector_dir / "numina.pkl")
    # indexer = FaissIndexer(index_path=index_path, texts_path=texts_path)
    # indexer.load()
    #
    # retrieved_texts_and_scores = indexer.search(query_vector, k=5)
    # # 输出一下看看
    # for text, score in retrieved_texts_and_scores:
    #     print(f"匹配文本：{text}\n相似度得分：{score}\n")
    # return jsonify({"content":"response_text"})

