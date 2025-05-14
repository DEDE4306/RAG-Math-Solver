#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)
# 加载 .env 文件

# 读取环境变量
# mysql 配置
PORT = int(os.getenv("PORT", 5000))
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
# 阿里云短信服务
access_key_id = os.getenv("ACCESS_KEY_ID")
access_key_secret = os.getenv("ACCESS_KEY_SECRET")
sign_name = os.getenv("SIGN_NAME")
template_code = os.getenv("TEMPLATE_CODE")
# 大模型 api
api_key = os.getenv("DASHSCOPE_API_KEY")

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", "6379")
redis_db = os.getenv("REDIS_DB", "0")
redis_password = os.getenv("REDIS_PASSWORD", "password")






