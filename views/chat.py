#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from flask import Blueprint, request

from models.db import db
from models.model import Session, Message
from utils.ai import chat_completion
from utils.auth import token_required, verify_token
from utils.response import flask_response

chat = Blueprint('chat', __name__, url_prefix='/api/chat')


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
    message = [{"role": "user", "content": content}]
    token = request.headers.get('Authorization')
    user_id = verify_token(token)
    result = chat_completion(message)
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


@chat.route('/sendMessage', methods=['POST'])
@token_required
def send_messgae():
    data = request.get_json()
    sessionid = data.get("sessionid")
    content = data.get("content")
    message = Message.query.filter_by(sessionid=sessionid).all()
    messages = [{"role": msg.role.value, "content": msg.content} for msg in message]
    result = chat_completion(messages)
    if result is False:
        return flask_response(code=500, message=f'ai服务器异常')

    save_message_db(sessionid, content, "user")
    msg2 = save_message_db(sessionid, result, "assistant")

    data = {
        "messageid": msg2.messageid,
        "role": msg2.role.value,
        "content": result,
        "createdat": msg2.createdat.strftime("%Y-%m-%d %H:%M:%S")
    }

    return flask_response(code=200, message=f'AI返回成功', data=data)


@chat.route('/getMessageListBySessionid/<sessionid>', methods=['GET'])
@token_required
def get_messgae(sessionid):
    message = Message.query.filter_by(sessionid=sessionid).all()
    messages = [{"role": msg.role.value, "content": msg.content, "messageid": msg.messageid,
                 "createdat": msg.createdat.strftime("%Y-%m-%d %H:%M:%S")} for msg in message]

    return flask_response(code=200, message=f'返回所有的会话消息成功', data=messages)


@chat.route('/getHistoricalSessions', methods=['GET'])
@token_required
def get_history_session():
    session = Session.query.all()
    messages = [{"sessionid": msg.sessionid, "title": msg.title} for msg in session]

    return flask_response(code=200, message=f'返回所有的会话列表成功', data=messages)


@chat.route('/editHistoricalMessage/<messageid>', methods=['PUT'])
@token_required
def edit_hostory_message(messageid):
    data = request.get_json()
    content = data.get("content")

    message1 = Message.query.filter_by(messageid=int(messageid)).first()
    sessionid = message1.sessionid

    # 更新
    message1.content = content

    # 删除下面的消息
    Message.query.filter(Message.sessionid == sessionid, Message.messageid > int(messageid)).delete()
    db.session.commit()

    message = Message.query.filter(Message.sessionid == sessionid, Message.messageid <= int(messageid)).all()
    messages = [{"role": msg.role.value, "content": msg.content} for msg in message]
    result = chat_completion(messages)
    if result is False:
        return flask_response(code=500, message=f'ai服务器异常')

    save_message_db(sessionid, result, "assistant")
    new_message = Message.query.filter_by(sessionid=sessionid).all()
    messages = [{"role": msg.role.value, "content": msg.content, "messageid": msg.messageid,
                 "createdat": msg.createdat.strftime("%Y-%m-%d %H:%M:%S")} for msg in new_message]

    return flask_response(code=200, message=f'返回当前会话消息列表成功', data=messages)
