#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from urllib.parse import quote

from config import *

redis = FlaskRedis()  # 延迟初始化模式
db = SQLAlchemy()

def init_db(app=None):
    """初始化数据库"""
    if not app:
        app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/rag'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    password = "123"
    encoded_password = quote(password, safe='')
    # app.config['REDIS_URL'] = f"redis://:{encoded_password}@127.0.0.1:6379/0"

    # 初始化Redis
    redis.init_app(app)

    db.init_app(app)
    return app


