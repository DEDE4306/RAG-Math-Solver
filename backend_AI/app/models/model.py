#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import binascii
import hashlib
from datetime import datetime
import os
from enum import Enum

from ..models.db import db, init_db
from werkzeug.security import generate_password_hash, check_password_hash




class User(db.Model):
    """用户模型"""
    __tablename__ = 'user'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    phonenumber = db.Column(db.String(20), nullable=False, unique=True)
    passwordhash = db.Column(db.String(64), nullable=False)
    avatarUrl = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # 索引定义
    __table_args__ = (
        db.Index('idx_username', 'username'),
        db.Index('idx_phonenumber', 'phonenumber'),
    )

    def set_password(self, password):
        """生成密码哈希"""

        p = password
        for _ in range(102):
            p = hashlib.sha256(p.encode()).hexdigest()

        self.passwordhash = p

    def check_password(self, db_pwd, password):
        """验证密码"""
        p = password
        for _ in range(102):
            p = hashlib.sha256(p.encode()).hexdigest()

        return db_pwd == p

    def to_dict(self):
        """转换为字典（用于JSON序列化）"""
        return {
            'id': self.id,
            'username': self.username,
            'phonenumber': self.phonenumber,
            'avatarUrl': self.avatarUrl,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class RoleEnum(Enum):
    USER = 'user'
    ASSISTANT = 'assistant'


class Session(db.Model):
    __tablename__ = 'session'

    sessionid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    createdat = db.Column(db.DateTime, server_default=db.func.now())
    updatedat = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # 关系定义（假设User模型存在）
    user = db.relationship('User', backref=db.backref('sessions', lazy=True, cascade='all, delete-orphan'))

    # 定义索引
    __table_args__ = (
        db.Index('idx_userid', 'userid'),
        db.Index('idx_updatedat', 'updatedat'),
    )


class Message(db.Model):
    __tablename__ = 'message'

    messageid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sessionid = db.Column(db.Integer, db.ForeignKey('session.sessionid', ondelete='CASCADE'), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False)
    content = db.Column(db.Text, nullable=False)
    createdat = db.Column(db.DateTime, server_default=db.func.now())

    # 关系定义
    session = db.relationship('Session', backref=db.backref('messages', lazy=True, cascade='all, delete-orphan'))

    # 定义索引
    __table_args__ = (
        db.Index('idx_sessionid', 'sessionid'),
        db.Index('idx_createdat', 'createdat'),
    )


if __name__ == '__main__':
    # 必须在应用上下文中使用模型
    app = init_db()
    with app.app_context():
        db.create_all()