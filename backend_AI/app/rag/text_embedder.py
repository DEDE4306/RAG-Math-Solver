import pandas as pd
from embedder import Embedder

class TextDatasetEmbedder:
    def __init__(self, file_path, text_column):
        """
        构造函数
        :param file_path: 要加载的 CSV 文件路径
        :param text_column: 指定包含文本的列名
        """
        self.file_path = file_path
        self.text_column = text_column
        self.texts = self._load_texts()
        self.embedder = Embedder()

    def _load_texts(self):
        df = pd.read_csv(self.file_path)
        return df[self.text_column].dropna().tolist()

    def get_embeddings(self):
        return self.embedder.embed(self.texts), self.texts  # 返回文本的向量表示和原始文本