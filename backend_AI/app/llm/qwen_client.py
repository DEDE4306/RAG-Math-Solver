from openai import OpenAI

class QwenClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"  # 填写DashScope服务的base_url

    def chat(self, messages):
        """
        messages: List[Dict]，每条包含 'role' 和 'content'，如：
        [
            {"role": "system", "content": "你是一个精通数学的AI..."},
            {"role": "user", "content": "请解释勾股定理"},
            {"role": "assistant", "content": "勾股定理是..."},
            {"role": "user", "content": "它的应用有哪些？"}
        ]
        """
        client = OpenAI(
            api_key=self.api_key,  # 使用的 api_key
            base_url=self.base_url,  # 填写DashScope服务的base_url
        )
        completion = client.chat.completions.create(
            model="qwen-math-plus",
            messages=messages
            # stream = True,  # 开启流式输出
        )
        answer = completion.choices[0].message.content
        print(answer) # 返回纯文本内容
        return answer

        # answer = ""
        # for chunk in completion:
        #     try:
        #         content = chunk.choices[0].delta.content
        #         answer += content
        #         print(content, end="", flush=True)  # 实时打印
        #     except KeyError:
        #         continue
        # print()  # 换行
        # return answer