# views/send_message.py
from datetime import datetime
from flask import Blueprint,request,jsonify
from ..rag.embedder import Embedder
from ..rag.faiss_indexer import FaissIndexer
from ..llm.qwen_client import QwenClient
from ..models.db import db
from ..models.model import Message
from pathlib import Path
from config import api_key

chat = Blueprint('chat', __name__, url_prefix='/api/chat') # 创建一个聊天蓝图


@chat.route('/sendMessage',methods=['POST'])
def send_message():
    # try:
        # 获取数据
        data = request.get_json()
        user_question = data.get('content')
        sessionid = data.get('sessionid')

        # 向量化用户提问
        embedder = Embedder(model_name="BAAI/bge-large-zh-v1.5")
        query_vector = embedder.embed(user_question)

        # 获取向量化数据
        vector_dir = Path(__file__).parent.parent / "vector"  # vector 在项目根目录下
        # print(vector_dir)
        index_path = str(vector_dir / "formula.index")
        texts_path = str(vector_dir / "formula.pkl")
        indexer = FaissIndexer(index_path=index_path, texts_path=texts_path)
        indexer.load()

        # 检索 top-k 上下文
        retrieved_texts_and_scores = indexer.search(query_vector,k=5)
        context = "\n".join([f"- {text}" for text, _ in retrieved_texts_and_scores])


        # 构造提示词（Prompt）
        prompt = f"请回答问题：\n{user_question}\n\n以下是一些相关的数学知识片段：\n{context}"
        print(prompt)


        # if len(prompt) > 3072:
        #     prompt = prompt[:3072]
        # print("prompt 过长，进行截断")

        # 调用模型
        qwen_client = QwenClient(api_key=api_key)
        response_text = qwen_client.chat(prompt)

        # user_message = Message(
        #     sessionid=sessionid,
        #     role='user',
        #     content=user_question,
        #     createdat=datetime.now()
        # )
        # db.session.add(user_message)
        #
        # assistant_message = Message(
        #     sessionid=sessionid,
        #     role='assistant',
        #     content=response_text,
        #     createdat=datetime.now()
        # )
        # db.session.add(assistant_message)
        #
        # db.session.commit()

        message_id = 0

        # 返回前端
        result = {
            "success": True,
            "msg": "请求成功",
            "response":{
                "messageid":message_id,
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