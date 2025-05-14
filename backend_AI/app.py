# app.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask

from config import PORT


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'static/avatars'
    app.config['SECRET_KEY'] = 'qw-passwd-key'
    app.config['JWT_ALGORITHM'] = 'HS256'

    # 初始化数据库
    from app.models.db import init_db
    init_db(app)

    # 蓝图注册延迟到应用创建后
    from app.views.user import account
    app.register_blueprint(account)
    from app.views.send_message import chat
    app.register_blueprint(chat)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=PORT, debug=True)

"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from config import PORT
from models.db import init_db



app.config['UPLOAD_FOLDER'] = 'static/avatars'
app.config['SECRET_KEY'] = 'qw-passwd-key'
app.config['JWT_ALGORITHM'] = 'HS256'

# 初始化数据库
init_db(app)

# 注册蓝图
app.register_blueprint(account)
app.register_blueprint(chat)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False)

"""
