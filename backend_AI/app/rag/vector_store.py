# vector_store.py
# 将我的数据集转化为向量的脚本
# from text_embedder import TextDatasetEmbedder
# from faiss_indexer import FaissIndexer
#
#
# dataset = TextDatasetEmbedder('../data/numina.csv',
#                                           ['problem','solution'],
#                                           "问题：{problem}，解答：{solution}")
# indexer = FaissIndexer(index_path='../vector/numina.index',texts_path='../vector/numina.pkl')
# indexer.build_from_dataset(dataset)
# indexer.save()


# vector_store.py
# 将我的数据集转化为向量的脚本
import argparse
from text_embedder import TextDatasetEmbedder
from faiss_indexer import FaissIndexer


def build_vector_store(data_path, columns, template, index_path, texts_path,file_type):
    dataset = TextDatasetEmbedder(data_path, columns, template,file_type)
    indexer = FaissIndexer(index_path=index_path, texts_path=texts_path)
    indexer.build_from_dataset(dataset)
    indexer.save()
    print(f"向量化成功，已保存到{index_path}、{texts_path}")


if __name__ == "__main__":
    build_vector_store("../data/formula.json",  ["type","content"], "知识名称：{type}，描述：{content}"
                       , "../vector/formula.index", "../vector/formula.pkl","json")

