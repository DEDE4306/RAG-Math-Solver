from openai import OpenAI
import requests
import json


from config import api_key, model



def chat_completion(messages):
    url = "https://api.siliconflow.cn/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 512
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()
        content = result['choices'][0]['message']['content']
        print("AI回复：", content)
        return content
    else:
        print("报错:", response.status_code)
        print(response.text)
        return False



