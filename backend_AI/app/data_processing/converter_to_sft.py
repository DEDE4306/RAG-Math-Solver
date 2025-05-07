import json

def convert_to_sft_format(old_data):
    sft_data = []
    for item in old_data:
        user_content = (
            f"{item['question']}  {item['options']}"
        )
        assistant_content = f"本题正确答案为 {item['answer']}。{item['analysis'].strip()}" if (
                item['analysis'] and item['analysis'].lower() != 'null') else f"本题正确答案为 {item['answer']}。"
        sft_data.append({
            "messages": [
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": assistant_content}
            ]
        })
    return sft_data

# 读取原始数据
# with open('../data/train_data.jsonl', 'r', encoding='utf-8') as f:
#     raw_data = json.load(f)
with open('../data/train_data.jsonl', 'r', encoding='utf-8') as f:
    raw_data = [json.loads(line) for line in f]

# 转换
sft_data = convert_to_sft_format(raw_data)

# 保存为新文件
# with open('../data/sft_chatml_questions.json', 'w', encoding='utf-8') as f:
#     for item in sft_data:
#         f.write(json.dumps(item, ensure_ascii=False) + '\n')
with open('../data/sft_chatml_questions.jsonl', 'w', encoding='utf-8') as f:
    for item in sft_data:
        # 将 python 对象转换为 json 字符串
        json_line = json.dumps(item, ensure_ascii=False) # ensure_ascii = False 可以保留中文
        f.write(json_line + '\n')