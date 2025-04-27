# vector_store.py
from text_embedder import TextDatasetEmbedder
from faiss_indexer import FaissIndexer


dataset = TextDatasetEmbedder('../data/numina.csv',
                                          ['problem','solution'],
                                          "问题：{problem}，解法：{solution}")
indexer = FaissIndexer(index_path='../vector/numina.index',texts_path='../vector/numina.pkl')
indexer.build_from_dataset(dataset)
indexer.save()


