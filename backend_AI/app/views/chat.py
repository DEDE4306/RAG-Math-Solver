#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# views/chat.py
import uuid
import os
from datetime import datetime
from flask import Blueprint,request,jsonify
from ..llm.qwen_client import QwenClient
from ..utils.ai import chat_completion
from ..utils.auth import token_required, verify_token
from ..utils.response import flask_response
from ..utils.ocr import BaiduOCRClient
from ..models.db import db
from ..models.model import Session, Message
from pathlib import Path
from config import api_key


chat = Blueprint('chat', __name__, url_prefix='/api/chat') # 创建一个聊天蓝图

def save_message_db(sessionid, content, role):
    msg = Message(
        content=content,
        role=role,
        sessionid=sessionid,
        createdat=datetime.now(),
    )

    db.session.add(msg)
    db.session.commit()
    return msg

@chat.route('/createNewSession', methods=['POST'])
@token_required
def create_new_session():
    data = request.get_json()
    content = data.get("content")
    token = request.headers.get('Authorization')
    user_id = verify_token(token)
    result = chat_completion(content)
    if result is False:
        return flask_response(code=500, message=f'ai服务器异常')

    session = Session(
        title=content,
        userid=user_id,
        createdat=datetime.now(),
        updatedat=datetime.now()
    )
    db.session.add(session)
    db.session.commit()

    msg1 = Message(
        content=content,
        role="user",
        sessionid=session.sessionid,
        createdat=datetime.now(),
    )

    msg2 = Message(
        content=result,
        role="assistant",
        sessionid=session.sessionid,
        createdat=datetime.now(),
    )

    db.session.add(msg1)
    db.session.add(msg2)
    db.session.commit()

    data = {
        "sessionid": session.sessionid,
        "title": content,
        "messages": [{"messageid": msg1.messageid, "role": msg1.role.value, "content": msg1.content,
                      "createdat": msg1.createdat.strftime("%Y-%m-%d %H:%M:%S")},
                     {"messageid": msg2.messageid, "role": msg2.role.value, "content": msg2.content,
                      "createdat": msg2.createdat.strftime("%Y-%m-%d %H:%M:%S")}]
    }

    return flask_response(code=200, message=f'AI返回成功', data=data)

@chat.route('/sendMessage',methods=['POST'])
@token_required
def send_message():
    # try:
        # 获取数据
        data = request.get_json()
        content = data.get('content')
        sessionid = data.get('sessionid')

        result = chat_completion(content)

        save_message_db(sessionid, content, "user")
        msg2 = save_message_db(sessionid, result, "assistant")

        # 返回前端
        data = {
            "messageid":msg2.messageid,
            "role":msg2.role.value,
            "content":result,
            "createdat":msg2.createdat.strftime("%Y-%m-%d %H:%M:%S")
        }
        return flask_response(code=200, message='消息发送成功', data=data)


    # except Exception as e:
    #     return jsonify({
    #         "success": False,
    #         "msg": f"服务异常：{str(e)}",
    #         "response": {}
    #     })


@chat.route('/ocr', methods=['POST'])
def ocr_extract():
    if 'file' not in request.files:
        return flask_response(code=400, message='缺少上传文件')

    file = request.files['file']
    if file.filename == '':
        return flask_response(code=400, message='文件名为空')

    allowed_exts = ['jpg', 'jpeg', 'png', 'gif', 'bmp']
    ext = file.filename.rsplit('.', 1)[-1].lower()
    if ext not in allowed_exts:
        return flask_response(code=400, message='不支持的文件格式')

    filename = f"{uuid.uuid4()}.{ext}"
    app_path = Path(__file__).parent.parent
    upload_dir = os.path.join(app_path, "static", "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    save_path = os.path.join(upload_dir, filename)
    file.save(save_path)

    ocr_client=BaiduOCRClient()

    try:
        result = ocr_client.analyze_document(save_path)
        data = [item.get('words') for item in result.get("words_result", [])]
        text = "\n".join(data)
        return flask_response(code=200, message='消息发送成功', data=text)
    except Exception as e:
        return flask_response(code=500, message=f'OCR 识别失败：{str(e)}')