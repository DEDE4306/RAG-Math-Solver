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

    return token


def verify_token(token):
    """验证JWT Token"""
    try:
        # print(f"the token sent:{token}")
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        # print(f"verify token:{payload['user_id']}")
        return payload['user_id']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        # print(f"verify token:{token}")
        return None


def get_user_id():
    """获取用户ID"""
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token.split(' ')[1]
    user_id = verify_token(token)
    return user_id


# def token_required(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         # print(request.headers)
#         token = request.headers.get('Authorization')
#         # print("token:", token)
#         user_id = get_user_id()
#         _token = LoginToken.get_token(user_id)
#         if _token != token:
#             return flask_response(code=401, message=f'token已过期')
#         if not token:
#             return flask_response(code=401, message=f'无token')
#         user_id = verify_token(token)
#         if not user_id:
#             return flask_response(code=401, message=f'失效的token')
#         if kwargs:
#             return func(**kwargs)
#
#         return func()
#
#     return wrapper
def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # print("========== 进入 token_required ==========")

        # 打印整个请求头，用于调试
        # print("请求头 (request.headers):")
        # print(request.headers)

        # 放行 OPTIONS 请求
        if request.method == 'OPTIONS':
            # print("[INFO] 检测到 OPTIONS 请求，直接放行")
            return func(*args, **kwargs)

        # 获取 Token 并移除 'Bearer ' 前缀
        auth_header = request.headers.get('Authorization')
        # print(f"[DEBUG] Authorization Header: {auth_header}")

        if not auth_header:
            # print("[ERROR] 无 Authorization 请求头")
            return flask_response(code=401, message='无token')

        if not auth_header.startswith('Bearer '):
            # print("[ERROR] Authorization 格式错误，必须以 'Bearer ' 开头")
            return flask_response(code=401, message='无效的token格式')

        token = auth_header.split(' ')[1]
        # print(f"[DEBUG] 提取的 Token: {token}")

        if not token:
            # print("[ERROR] 提取到的 Token 为空")
            return flask_response(code=401, message='无token')

        # 解析 Token 获取 user_id
        user_id = verify_token(token)
        # print(f"[DEBUG] 解析得到的 user_id: {user_id}")

        if not user_id:
            # print("[ERROR] Token 验证失败，可能是过期或无效 Token")
            return flask_response(code=401, message='失效的token')

        # 检查 Token 是否和数据库中的一致
        db_token = LoginToken.get_token(user_id)
        # print(f"[DEBUG] 数据库中存储的 Token: {db_token}")

        if db_token != token:
            # print("[ERROR] Token 不一致，可能已过期或被其他设备登录覆盖")
            return flask_response(code=401, message='token已过期')

        # print("[SUCCESS] Token 验证通过，开始执行接口逻辑")

        # 执行真正的函数
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
        # cls.set_code(phone_number, int(code))
        # return code
        if send_sms(phone_number, code):
            cls.set_code(phone_number, int(code))
            print(f"发送验证码 {code} 到 {phone_number}")
            return code
        else:
            print(f"发送到 {phone_number} 验证码失败")

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
        print(user_id, token)
        cls.token_dict[user_id] = token

    @classmethod
    def get_token(cls, user_id):
        print(f"user_id:{user_id},token:{cls.token_dict.get(user_id)}")
        return cls.token_dict.get(user_id)

    @classmethod
    def del_token(cls, user_id):
        cls.token_dict.pop(user_id, None)


if __name__ == '__main__':
    print()
    print(verify_token(generate_token(1)))
