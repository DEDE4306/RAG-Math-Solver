#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import uuid

from flask import Blueprint, request, current_app, send_from_directory, url_for
from flask_cors import cross_origin

from pathlib import Path

from config import PORT
from app.models.db import db
from app.models.model import User  # 导入用户模型
from app.utils.auth import generate_token, token_required, verify_token, get_user_id, PhoneCode, LoginToken
from app.utils.response import flask_response


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
            filename = f"{uuid.uuid4()}.{ext}"
            # filename = file.filename
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

    try:
        db.session.add(new_user)
        db.session.commit()

        # 生成token
        token = generate_token(new_user.id)
        PhoneCode.del_code(phone)
        return flask_response(code=200, message=f'注册成功', data={"token": token})

    except Exception as e:
        db.session.rollback()
        print(str(e))
        return flask_response(code=500, message='注册失败: ' + str(e))


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
    # token = request.headers.get('Authorization')
    # print("the token is {}".format(token))
    # user_id = verify_token(token)
    user_id = get_user_id()
    # print(f"[DEBUG] Parsed user_id from token: {user_id}")
    user = User.query.filter_by(id=user_id).first()

    image_filename = os.path.basename(user.avatarUrl)
    # 生成图片的 URL
    image_url = url_for('user.get_uploaded_file', filename=f'{image_filename}')

    data = {
        'avatarUrl': f"http://100.42.205.158:{PORT}" + image_url,
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
    user = User.query.get(user_id)
    # 处理头像更新
    if 'newAvatarFile' in request.files:
        # 删除旧头像文件（如果存在）
        if user.avatarUrl:
            old_avatar_path = Path(__file__).parent.parent / user.avatarUrl.lstrip('/')
            if old_avatar_path.exists():
                os.remove(old_avatar_path)
        # 处理头像上传
        file = request.files['newAvatarFile']
        # 保存文件到服务器
        if file and file.filename.split(".")[-1] in ['jpg', 'png', 'jpeg', 'gif']:
            # 生成唯一文件名
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4()}.{ext}"
        else:
            return  flask_response(code=400, message=f'请上传正确的文件格式')

        app_path = Path(__file__).parent.parent
        file.save(os.path.join(app_path, "static", "avatars", filename))
        user.avatarUrl = f"/static/avatars/{filename}"
    # 处理用户名更新
    if 'newUsername' in request.form:
        user.username = request.form['newUsername']
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

# @token_required
@account.route('/img/<filename>')
@cross_origin()  # 允许跨域请求
def get_uploaded_file(filename):
    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'])
    # print(f"[DEBUG] Looking for file: {filename} in directory: {upload_dir}")
    if not os.path.exists(os.path.join(upload_dir, filename)):
        # print("[ERROR] File does not exist.")
        return "File not found", 404
    return send_from_directory(upload_dir, filename)
