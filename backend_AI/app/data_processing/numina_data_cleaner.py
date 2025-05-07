# numina_data_cleaner.py
import pandas as pd
import re
import json
import os

class NuminaDataCleaner:
    def __init__(self, input_path, output_path=None):
        self.input_path = input_path
        self.output_path = output_path or self._default_output_path()
        print(self.output_path)

    def _default_output_path(self):
        base, ext = os.path.splitext(self.input_path)
        return f"{base}_cleaned{ext}"

    def clean_text(self, text):
        if not isinstance(text, str):
            return ""
        text = text.strip()
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'\s+', ' ', text)
        return text

    def is_valid_row(self, row):
        if not row['problem'] or not row['solution']:
            return False
        if "undefined" in row['solution'].lower():
            return False
        try:
            _ = json.loads(row['messages'].replace("'", '"'))
        except:
            return False
        return True

    def clean(self):
        df = pd.read_csv(self.input_path)

        # 保留 source 为 cn_k12 的数据
        if 'source' in df.columns:
            df = df[df['source'] == 'cn_k12']

        # 清洗文本字段
        df['problem'] = df['problem'].apply(self.clean_text)
        df['solution'] = df['solution'].apply(self.clean_text)
        df['messages'] = df['messages'].apply(self.clean_text)

        # 过滤无效行
        df = df[df.apply(self.is_valid_row, axis=1)]

        # 去重
        df.drop_duplicates(subset=['problem', 'solution'], inplace=True)

        # 保存
        df.to_csv(self.output_path, index=False)
        print(f"清洗完成，保存至: {self.output_path}")

