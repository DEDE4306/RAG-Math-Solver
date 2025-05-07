from flask import Flask

def create_app():
    app = Flask(__name__)

    # 配置项，比如 app.config['SECRET_KEY'] = 'your_secret_key'
    # app.config.from_pyfile('../config.py')  # 如果你有 config 文件的话
    #
    # # 蓝图注册（下面我再讲蓝图怎么写）
    # from app.chat import chat_bp
    # app.register_blueprint(chat_bp, url_prefix='/chat')
    #
    # from app.login import login_bp
    # app.register_blueprint(login_bp, url_prefix='/auth')
    from app.api.send_message import chat_bp
    app.register_blueprint(chat_bp)

    return app