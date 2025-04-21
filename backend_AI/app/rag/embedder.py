# embedder.py
from sentence_transformers import SentenceTransformer
import torch

class Embedder:
    def __init__(self, model_name='BAAI/bge-large-en-v1.5', use_gpu=True):
        print("Loading embedding model...")
        self.device = 'cuda' if use_gpu and torch.cuda.is_available() else 'cpu'
        print('self.device = ' + self.device)
        self.model = SentenceTransformer(model_name,device=self.device)
        self.model.eval()

    def embed(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        embeddings = self.model.encode(texts, show_progress_bar=True, convert_to_tensor=True)
        return embeddings.cpu().numpy()