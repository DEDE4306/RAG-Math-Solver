# embedder.py
# 用于将数据集向量化
from sentence_transformers import SentenceTransformer
import torch


# 用于将数据集向量化
class Embedder:
    def __init__(self, model_name='BAAI/bge-large-zh-v1.5', use_gpu=True):
        print("Loading embedding model...")
        self.device = 'cuda' if use_gpu and torch.cuda.is_available() else 'cpu'
        print('self.device = ' + self.device)
        self.model = SentenceTransformer(model_name,device=self.device)
        self.model.eval()

    # 将数据集向量化
    def embed(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        embeddings = self.model.encode(texts, show_progress_bar=False, convert_to_tensor=True)
        # print(embeddings.cpu().numpy())
        return embeddings.cpu().numpy()