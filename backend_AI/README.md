# Arithmetic and Mathematical Problem Solving Assistant Based on RAG and LLM

## 项目简介

这是一个基于 RAG（Retrieval-Augmented Generation）与大型语言模型（LLM）的数学问题求解助手。用户可以通过文字输入数学问题，系统会结合知识库中的公式与定理进行推理并给出详细的解答步骤。此外，支持图像识别（OCR）、多轮对话以及历史记录管理等功能，适用于学习辅助、教学答疑等场景。

## 功能 Features
- 用户注册：输入手机号、验证码、密码、用户名和头像，进行注册
- 用户登录：通过密码或者验证码进行登录
- 更新用户信息：修改头像、用户名、手机号或密码。
- 选择会话查看历史消息：回顾以往的对话内容。
- 开启新会话：开始新的问答流程。
- 上传图片识别文字：通过 OCR 提取图像中的数学表达式。
- 发送消息与模型对话：与 AI 助手实时互动。
- 编辑历史消息：重新编辑历史消息，让模型重新回答

## 技术栈 Tech Stack
- Python 3.8
- Flask
- SQLAlchemy
- Flask-Migrate
- MySQL
- FAISS

## 环境准备与安装 Installation

1. 克隆项目
```bash
git clone https://github.com/DEDE4306/RAG-Math-Solver.git
cd RAG-Math-Solver
```
2. 创建虚拟环境并安装依赖

```bash
python3 -m venv .venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
3. 创建数据库
```sql
CREATE TABLE User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) NOT NULL UNIQUE,
    phonenumber VARCHAR(20) NOT NULL UNIQUE,
    passwordhash VARCHAR(64) NOT NULL,
    avatarUrl VARCHAR(255),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_phonenumber (phonenumber)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```
```sql
CREATE TABLE Session (
    sessionid INT AUTO_INCREMENT PRIMARY KEY,
    userid INT NOT NULL,
    title VARCHAR(30) NOT NULL,
    createdat DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedat DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (userid) REFERENCES User(id) ON DELETE CASCADE,
    INDEX idx_userid (userid),
    INDEX idx_updatedat (updatedat)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```
```sql
CREATE TABLE Message (
    messageid INT AUTO_INCREMENT PRIMARY KEY,
    sessionid INT NOT NULL,
    role ENUM('user', 'assistant') NOT NULL,
    content TEXT NOT NULL,
    createdat DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sessionid) REFERENCES Session(sessionid) ON DELETE CASCADE,
    INDEX idx_sessionid (sessionid),
    INDEX idx_createdat (createdat)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```
4. 运行
```shell
python app.py
```




