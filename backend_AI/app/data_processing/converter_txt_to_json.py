import json
import re

def txt_to_json(txt_path, json_path):
    new_data = []
    with open(txt_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line or not line.startswith('type:'):
                continue
            # 简单解析 type 和 content
            try:
                type_part, content_part = line.split('content:', 1)
                type_value = type_part.replace('type:', '').strip()
                content_value = content_part.strip()
                new_data.append({
                    'type': type_value,
                    'content': content_value
                })
            except ValueError:
                print(f"无法解析行：{line}")

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    existing_contents = set(item['content'] for item in existing_data)
    merged_data = existing_data.copy()
    for item in new_data:
        if item['content'] not in existing_contents:
            merged_data.append(item)
            existing_contents.add(item['content'])

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)

    print(f"追加完成，共保存 {len(merged_data)} 条数据。")

txt_to_json('../data/数据_2.txt', '../data/formula.json')
# 示例用法
# append_to_json("math_knowledge.json", "new_entries.txt")