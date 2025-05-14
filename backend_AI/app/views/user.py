#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

from flask import Blueprint, request, current_app, send_from_directory, url_for

from config import PORT
from app.models.db import db
from app.models.model import User  # 导入用户模型
from app.utils.auth import generate_token, token_required, verify_token, get_user_id, PhoneCode, LoginToken
from app.utils.response import flask_response
from pathlib import Path

account = Blueprint('user', __name__, url_prefix='/api/account')


def validate_phone(phone):
    """验证手机号格式"""
    return re.match(r'^1[3-9]\d{9}$', phone) is not None


@account.route('/register', methods=['POST'])
def register():
    """用户注册接口"""
    # 验证必需参数
    required_fields = ['phonenumber', 'code', 'username', 'password']
    for field in required_fields:
        if field not in request.form:
            return flask_response(code=400, message=f'缺少必需参数: {field}')

    # 获取参数
    phone = request.form['phonenumber']
    code = request.form['code']
    username = request.form['username']
    password = request.form['password']

    # 参数验证
    if not validate_phone(phone):
        return flask_response(code=400, message=f'手机号格式不正确')

    if len(password) < 6 or len(password) > 20:
        return flask_response(code=400, message=f'密码长度应在6-20个字符之间')

    # TODO: 验证码校验逻辑（实际项目需要实现）
    if not PhoneCode.check_code(phone, code):
        return flask_response(code=400, message=f'验证码错误')

    # 检查用户是否已存在
    if User.query.filter_by(phonenumber=phone).first():
        return flask_response(code=400, message=f'该手机号已注册')

    if User.query.filter_by(username=username).first():
        return flask_response(code=400, message=f'用户名已存在')

    # 处理头像上传
    avatar_url = None
    if 'avatar' in request.files:
        file = request.files['avatar']
        if file and file.filename.split(".")[-1] in ['jpg', 'png', 'jpeg', 'gif']:
            # 生成唯一文件名
            ext = file.filename.rsplit('.', 1)[1].lower()
            # filename = f"{uuid.uuid4()}.{ext}"
            filename = file.filename
            app_path = Path(__file__).parent.parent
            file.save(os.path.join(app_path,"static","avatars", filename))
            avatar_url = f"/static/avatars/{filename}"

    # 创建用户
    new_user = User(
        phonenumber=phone,
        username=username,
        avatarUrl=avatar_url
    )
    new_user.set_password(password)

    # try:
    db.session.add(new_user)
    db.session.commit()

        # 生成token
    token = generate_token(new_user.id)
    PhoneCode.del_code(phone)
    return flask_response(code=200, message=f'注册成功', data={"token": token})

    # except Exception as e:
    # db.session.rollback()
    # print(str(e))
    # return flask_response(code=500, message='注册失败: ' + str(e))


@account.route('/sendCode', methods=['POST'])
def sendCode():
    """
    请求发送验证码
    :return:
    """
    data = request.get_json()
    phonenumber = data.get('phonenumber')
    if PhoneCode.send_code(phonenumber):
        return flask_response(code=200, message='验证码发送成功')
    else:
        return flask_response(code=500, message='验证码发送失败')


@account.route('/loginWithCode', methods=['POST'])
def loginWithCode():
    """
    验证码登录
    :return:
    """
    data = request.get_json()
    phonenumber = data.get('phonenumber')
    code = data.get('code')
    if not PhoneCode.check_code(phonenumber, code):
        return flask_response(code=400, message=f'验证码错误')

    user = User.query.filter_by(phonenumber=phonenumber).first()
    token = generate_token(user.id)
    LoginToken.set_token(user.id, token)
    return flask_response(code=200, message='登陆成功', data={"token": token, "username": user.username})


@account.route('/loginWithPassword', methods=['POST'])
def loginWithPassword():
    """
    密码登录
    :return:
    """
    data = request.get_json()

    if not User.query.filter_by(phonenumber=data['phonenumber']).first():
        return flask_response(code=404, message='用户不存在')

    user = User.query.filter_by(phonenumber=data['phonenumber']).first()

    if not User().check_password(user.passwordhash, data['password']):
        return flask_response(code=400, message='密码错误')

    user = User.query.filter_by(phonenumber=data['phonenumber']).first()
    token = generate_token(user.id)
    LoginToken.set_token(user.id, token)
    return flask_response(code=200, message=f'登录成功', data={"token": token, "username": user.username})


@account.route('/getBasicUserInfo', methods=['GET'])
@token_required
def getBasicUserInfo():
    """获取基本用户信息"""
    token = request.headers.get('Authorization')
    print("the token is {}".format(token))
    user_id = verify_token(token)
    user = User.query.filter_by(id=user_id).first()

    image_filename = os.path.basename(user.avatarUrl)
    # 生成图片的 URL
    image_url = url_for('user.get_uploaded_file', filename=f'{image_filename}')

    data = {
        'avatarUrl': f"http://localhost:{PORT}" + image_url,
        'username': user.username,
        'phonenumber': user.phonenumber,
    }
    return flask_response(code=200, message='查询基本信息成功', data=data)


@account.route('/changeBasicUserInfo', methods=['PUT'])
@token_required
def changeBasicUserInfo():
    """
    更新基本用户信息

    :return:
    """
    user_id = get_user_id()
    newAvatarFile = request.form.get("newAvatarFile")
    newUsername = request.form.get("newUsername")

    user = User.query.get(user_id)
    if newAvatarFile:
        user.avatarUrl = newAvatarFile
    if newUsername:
        user.username = newUsername
    db.session.commit()
    return flask_response(code=200, message='更新基本信息成功')


@account.route('/changePhoneNumber', methods=['PUT'])
@token_required
def changePhoneNumber():
    """
    更新手机号
    :return:
    """
    data = request.get_json()
    user_id = get_user_id()
    newPhonenumber = data.get("newPhonenumber")
    code = data.get("code")
    # TODO 校验验证码
    if not PhoneCode.check_code(newPhonenumber, code):
        return flask_response(code=400, message=f'验证码错误')

    user = User.query.get(user_id)
    if newPhonenumber:
        user.phonenumber = newPhonenumber

    db.session.commit()
    return flask_response(code=200, message='更新手机号码成功')


@account.route('/changePassword', methods=['PUT'])
@token_required
def changePassword():
    """
    更新密码
    :return:
    """
    data = request.get_json()
    user_id = get_user_id()
    Phonenumber = data.get("phonenumber")
    newPassword = data.get("newPassword")
    code = data.get("code")

    if not PhoneCode.check_code(Phonenumber, code):
        return flask_response(code=400, message=f'验证码错误')

    user = User.query.get(user_id)
    if newPassword:
        user.set_password(newPassword)

    db.session.commit()
    return flask_response(code=200, message='更新密码成功')


@account.route('/img/<filename>')
@token_required
def get_uploaded_file(filename):
    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'])
    return send_from_directory(upload_dir, filename)
