import json

# def find_long_contents(file_path, length_threshold):
#     try:
#         with open(file_path, "r", encoding="utf-8") as f:
#             data = json.load(f)
#
#         long_contents = []
#         for i, item in enumerate(data):
#             content_length = len(item.get("content", ""))
#             if content_length > length_threshold:
#                 long_contents.append((i, item["type"], content_length))
#
#         if long_contents:
#             print(f"共找到 {len(long_contents)} 个超长条目：")
#             for idx, t, length in long_contents:
#                 print(f"索引: {idx}, 类型: {t}, 内容长度: {length}")
#         else:
#             print("没有找到超过指定长度的条目。")
#
#     except json.JSONDecodeError as e:
#         print(f"JSON 文件格式错误: {e}")
#     except Exception as e:
#         print(f"发生错误: {e}")
#
# # 设置文件路径和长度阈值（比如超过 300 字符）
# json_path = "../data/formula.json"
# length_threshold = 300
#
# find_long_contents(json_path, length_threshold)

import json

with open("../data/formula.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"共有 {len(data)} 条数据")
