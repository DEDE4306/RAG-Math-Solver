from openai import OpenAI

class QwenClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"  # 填写DashScope服务的base_url

    def chat(self, prompt):
        client = OpenAI(
            api_key=self.api_key,  # 使用的 api_key
            base_url=self.base_url,  # 填写DashScope服务的base_url
        )
        completion = client.chat.completions.create(
            model="qwen-math-plus",
            messages=[
                {'role': 'system', 'content': '你是一个精通数学的 AI，现在需要你为同学或老师解决小学到高中的数学问题'},
                {'role': 'user', 'content': prompt}]
        )
        answer = completion.choices[0].message.content
        print(answer) # 返回纯文本内容
        return answer