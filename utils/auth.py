#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import string
from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import current_app, request

from utils.response import flask_response
from utils.sms import send_sms


def generate_token(user_id):
    """生成JWT Token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


def verify_token(token):
    """验证JWT Token"""
    try:
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        return payload['user_id']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def get_user_id():
    """获取用户ID"""
    token = request.headers.get('Authorization')
    user_id = verify_token(token)
    return user_id


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        user_id = get_user_id()
        _token = LoginToken.get_token(user_id)
        if _token != token:
            return flask_response(code=401, message=f'token已过期')
        if not token:
            return flask_response(code=401, message=f'无token')
        user_id = verify_token(token)
        if not user_id:
            return flask_response(code=401, message=f'失效的token')
        if kwargs:
            return func(**kwargs)

        return func()

    return wrapper


class PhoneCode:
    code_dict = {}

    @classmethod
    def send_code(cls, phone_number):
        code = ''.join(random.choices(string.digits, k=6))
        if send_sms(phone_number, code):
            cls.set_code(phone_number, int(code))
            print(f"发送验证码 {code} 到 {phone_number}")
            return code
        else:
            print(f"发送到 {phone_number} 验证码失败")

    @classmethod
    def set_code(cls, phone_number, code):
        cls.code_dict[phone_number] = {"code": code, "expire_time": datetime.now() + timedelta(minutes=5)}

    @classmethod
    def get_code(cls, phone_number):
        code_info = cls.code_dict.get(phone_number)
        return code_info.get("code")

    @classmethod
    def check_code(cls, phone_number, code):
        code_info = cls.code_dict.get(phone_number, {})
        pre_code = code_info.get("code")
        expire_time = code_info.get("expire_time")
        if int(pre_code) == int(code) and datetime.now() < expire_time:
            return True
        else:
            return False

    @classmethod
    def del_code(cls, phone_number):
        cls.code_dict.pop(phone_number, None)


class LoginToken:
    token_dict = {}

    @classmethod
    def set_token(cls, user_id, token):
        cls.token_dict[user_id] = token

    @classmethod
    def get_token(cls, user_id):
        return cls.token_dict.get(user_id)

    @classmethod
    def del_token(cls, user_id):
        cls.token_dict.pop(user_id, None)


if __name__ == '__main__':
    print()
    print(verify_token(generate_token(1)))
