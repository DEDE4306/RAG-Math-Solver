import json

with open("../data/formula.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"共有 {len(data)} 条数据")
