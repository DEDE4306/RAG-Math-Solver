import base64
import requests
import urllib.parse
from config import ocr_api_key
from config import ocr_secret_key

class BaiduOCRClient:
    def __init__(self,api_key=ocr_api_key,secret_key=ocr_secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.access_token = self.get_access_token()

    def get_access_token(self):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key
        }
        response = requests.post(url, params=params)
        response.raise_for_status()
        return response.json().get("access_token")

    @staticmethod
    def image_to_base64(image_path, urlencoded = False):
        """
        :param image_path: 文件路径
        :return: base64 编码信息
        """
        with open(image_path, "rb") as f:
            content = base64.b64encode(f.read()).decode()
            if urlencoded:
                content = urllib.parse.quote_plus(content)
        return content

    def analyze_document(self, image_path):
        """
        调用百度 OCR 接口，返回 JSON 结果
        """
        url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/doc_analysis?access_token={self.access_token}"
        image_base64 = self.image_to_base64(image_path)
        payload = {
            "image": image_base64,
            "detect_direction": "true",
            "line_probability": "false",
            "disp_line_poly": "false",
            "words_type": "handprint_mix",
            "layout_analysis": "false",
            "recg_formula": "true",
            "recg_long_division": "false"
        }
        # 转为x-www-form-urlencoded字符串
        encoded_payload = urllib.parse.urlencode(payload)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        response = requests.post(url, data=encoded_payload, headers=headers)
        response.raise_for_status()
        return response.json()
