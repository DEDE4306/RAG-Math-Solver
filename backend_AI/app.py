# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# app.py


from flask import Flask
from flask_cors import CORS
from config import PORT
import os


def create_app():
    app = Flask(__name__)
    # 获取当前 app.py 所在目录（即 /home/ubuntu/wwwroot/RAG-Math-Solver/backend_AI/）
    basedir = os.path.abspath(os.path.dirname(__file__))

    # 设置 UPLOAD_FOLDER 为绝对路径
    app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'app', 'static', 'avatars')
    app.config['SECRET_KEY'] = 'qw-passwd-key'
    app.config['JWT_ALGORITHM'] = 'HS256'

    # 初始化数据库
    from app.models.db import init_db
    init_db(app)

    # 蓝图注册延迟到应用创建后
    from app.views.user import account
    app.register_blueprint(account)
    from app.views.chat import chat
    app.register_blueprint(chat)

    # 允许所有来源的跨域访问
    # CORS(app, resources={r"/*": {"origins":"*"}}) # 允许所有跨域请求
    CORS(app, resources={r"/*": {"origins": "*", "allow_headers": ["Content-Type", "Authorization"]}})

    return app

app = create_app()

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=PORT, debug=True)
