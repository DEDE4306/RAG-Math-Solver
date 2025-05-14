# utils/auth.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import string
from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import current_app, request

from .response import flask_response
from .sms import send_sms


def generate_token(user_id):
    """生成JWT Token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=2)
    }
    # 生成 Token，返回解码后的字符串
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

    # 如果是字节类型，进行解码
    if isinstance(token, bytes):
        token = token.decode('utf-8')

    return token


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
        print(f"发送验证码 {code} 到 {phone_number}")
        cls.set_code(phone_number, int(code))
        return code
        # if send_sms(phone_number, code):
        #     cls.set_code(phone_number, int(code))
        #     print(f"发送验证码 {code} 到 {phone_number}")
        #     return code
        # else:
        #     print(f"发送到 {phone_number} 验证码失败")

    @classmethod
    def set_code(cls, phone_number, code):
        cls.code_dict[phone_number] = {"code": code, "expire_time": datetime.now() + timedelta(minutes=5)}
        print(cls.code_dict)

    @classmethod
    def get_code(cls, phone_number):
        code_info = cls.code_dict.get(phone_number)
        return code_info.get("code")

    @classmethod
    def check_code(cls, phone_number, code):
        code_info = cls.code_dict.get(phone_number, {})
        pre_code = code_info.get("code")
        expire_time = code_info.get("expire_time")
        print(code, pre_code, expire_time)
        if pre_code is None or expire_time is None:
            print("错误: 该手机号不存在验证码")
            return False
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
