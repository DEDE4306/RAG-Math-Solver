import requests

BASE_URL = "110.42.205.158"

def get_token():
    login_url = f"{BASE_URL}/api/account/loginWithPassword"
    login_data = {
        "phonenumber": "12345678901",
        "password": "password123"
    }
    response = requests.post(login_url, json=login_data)
    assert response.status_code == 200
    return response.json()["response"]["token"]

def test_send_message():
    """测试 /api/chat/sendMessage 接口是否成功响应"""
    token = get_token()
    headers = {"Authorization": token}
    data = {
        "sessionid": 1,
        "content": "1+1等于几？"
    }
    response = requests.post(f"{BASE_URL}/api/chat/sendMessage", json=data, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True
    assert "content" in result["response"]

def test_ocr_image_upload():
    """测试 /api/chat/ocr 接口上传图片并返回识别结果"""
    token = get_token()
    headers = {"Authorization": token}
    files = {
        "image": open("tests/sample_image.png", "rb")  # 确保有一个图片放在 tests 目录
    }
    response = requests.post(f"{BASE_URL}/api/chat/ocr", headers=headers, files=files)
    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True
    assert "recognizedText" in result["response"]  # 假设你接口里这么叫
