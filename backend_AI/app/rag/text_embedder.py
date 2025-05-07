# text_embedder.py
# 将指定的 csv 文件向量化，目前支持的是将数据集中需要用到的两列拼接起来成为一句有逻辑的语句
import pandas as pd
from embedder import Embedder
import json

# 将指定的 csv 文件向量化，目前支持的是将数据集中需要用到的两列拼接起来成为一句有逻辑的语句
class TextDatasetEmbedder:
    def __init__(self,input_path,text_columns,prompt_template = "{text}", file_type = "csv"):
        self.input_path = input_path
        self.text_columns = text_columns
        self.prompt_template = prompt_template
        self.file_type = file_type.lower()
        self.embedder = Embedder()

    # 加载数据集中的 text，保存为一个 prompt
    def load_texts(self):
        texts = []

        if self.file_type == "csv":
            df = pd.read_csv(self.input_path).dropna(subset = self.text_columns)
            for _, row in df.iterrows():
                fields = {col: str(row[col]) for col in self.text_columns}
                fields.setdefault("text", "".join(fields.values()))
                texts.append(self.prompt_template.format(**fields))
        elif self.file_type == "json":
            with open(self.input_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for entry in data:
                fields = {col: str(entry.get(col, "")) for col in self.text_columns}
                fields.setdefault("text", "".join(fields.values()))
                texts.append(self.prompt_template.format(**fields))
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")
        return texts

    # 将文本向量化
    def get_embeddings(self):
        texts = self.load_texts()
        embeddings = self.embedder.embed(texts)
        return embeddings, texts