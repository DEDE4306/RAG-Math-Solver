import json

def txt_to_json(txt_path, json_path):
    result = []
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
                result.append({
                    'type': type_value,
                    'content': content_value
                })
            except ValueError:
                print(f"无法解析行：{line}")

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)


# 使用示例
txt_to_json('../data/数据.txt', '../data/formula.json')