# data_cleaning.py
import pandas as pd
import re
import json

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.strip()
    text = re.sub(r'\\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def is_valid_row(row):
    if not row['problem'] or not row['solution']:
        return False
    if "undefined" in row['solution'].lower():
        return False
    try:
        _ = json.loads(row['messages'].replace("'", '"'))
    except:
        return False
    return True

df = pd.read_csv("../data/numina_chunks/.csv")

# 清洗文本字段
df['problem'] = df['problem'].apply(clean_text)
df['solution'] = df['solution'].apply(clean_text)
df['messages'] = df['messages'].apply(clean_text)

# 过滤无效行
df = df[df.apply(is_valid_row, axis=1)]

# 去重
df.drop_duplicates(subset=['problem', 'solution'], inplace=True)