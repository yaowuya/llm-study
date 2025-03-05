import ast

import numpy as np
import pandas as pd
import tiktoken
from openai import OpenAI

from core.settings import settings

"""
向量化embedding
"""

OPEN_API_CLIENT = OpenAI(api_key=settings.open_api_key)


class Embedding:
    @classmethod
    def load_data(cls):
        input_datapath = "./apps/open_api/data/fine_food_reviews_1k.csv"
        df = pd.read_csv(input_datapath, index_col=0)
        df = df[["Time", "ProductId", "UserId", "Score", "Summary", "Text"]]
        df = df.dropna()

        # 将 "Summary" 和 "Text" 字段组合成新的字段 "combined"
        df["combined"] = "Title: " + df.Summary.str.strip() + "; Content: " + df.Text.str.strip()
        # print(df.head(2))
        # print(df["combined"])
        return df

    @classmethod
    def process_data(cls, df, embedding_encoding, max_tokens):
        """将样本减少到最近的1,000个评论，并删除过长的样本"""
        # 设置要筛选的评论数量为1000
        top_n = 1000
        # 对DataFrame进行排序，基于"Time"列，然后选取最后的2000条评论。
        # 这个假设是，我们认为最近的评论可能更相关，因此我们将对它们进行初始筛选。
        df = df.sort_values("Time").tail(top_n * 2)
        # 丢弃"Time"列，因为我们在这个分析中不再需要它。
        df.drop("Time", axis=1, inplace=True)
        # 从'embedding_encoding'获取编码
        encoding = tiktoken.get_encoding(embedding_encoding)

        # 计算每条评论的token数量。我们通过使用encoding.encode方法获取每条评论的token数，然后把结果存储在新的'n_tokens'列中。
        df["n_tokens"] = df.combined.apply(lambda x: len(encoding.encode(x)))

        # 如果评论的token数量超过最大允许的token数量，我们将忽略（删除）该评论。
        # 我们使用.tail方法获取token数量在允许范围内的最后top_n（1000）条评论。
        df = df[df.n_tokens <= max_tokens].tail(top_n)

        # 打印出剩余评论的数量。
        print(len(df))

    @staticmethod
    def embedding_text(text, model="text-embedding-ada-002"):
        """使用新方法调用 OpenAI Embedding API"""
        res = OPEN_API_CLIENT.embeddings.create(input=text, model=model)
        return res.data[0].embedding

    @classmethod
    def test_embedding(cls):
        # 新版本创建 Embedding 向量的方法
        # Ref：https://community.openai.com/t/embeddings-api-documentation-needs-to-updated/475663
        res = OPEN_API_CLIENT.embeddings.create(input="abc", model="text-embedding-ada-002")
        print(res.data[0].embedding)

    @classmethod
    def create_embedding(cls):
        """创建嵌入向量"""
        # 模型类型
        # 建议使用官方推荐的第二代嵌入模型：text-embedding-ada-002
        # embedding_model = "text-embedding-ada-002"
        # text-embedding-ada-002 模型对应的分词器（TOKENIZER）
        embedding_encoding = "cl100k_base"
        # text-embedding-ada-002 模型支持的输入最大 Token 数是8191，向量维度 1536
        # 在我们的 DEMO 中过滤 Token 超过 8000 的文本
        max_tokens = 8000
        df = cls.load_data()
        cls.process_data(df, embedding_encoding, max_tokens)
        # 向量化：实际生成会耗时几分钟，逐行调用 OpenAI Embedding API
        df["embedding"] = df.combined.apply(cls.embedding_text)
        output_datapath = "./apps/open_api/data/fine_food_reviews_with_embeddings_1k_1126.csv"
        df.to_csv(output_datapath)
        print(df["embedding"][0])

    @classmethod
    def search_by_embedding(cls, product_description):
        embedding_datapath = "./apps/open_api/data/fine_food_reviews_with_embeddings_1k_1126.csv"
        df_embedded = pd.read_csv(embedding_datapath, index_col=0)
        # 将字符串转换为向量
        df_embedded["embedding_vec"] = df_embedded["embedding"].apply(ast.literal_eval)
        cls.search_reviews(df_embedded, product_description, n=3)

    @staticmethod
    def cosine_similarity(a, b):
        # cosine_similarity 函数计算两个嵌入向量之间的余弦相似度。
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    @classmethod
    def search_reviews(cls, df, product_description, n=3, pprint=True):
        # 定义一个名为 search_reviews 的函数，
        # Pandas DataFrame 产品描述，数量，以及一个 pprint 标志（默认值为 True）。
        product_embedding = cls.embedding_text(product_description)

        df["similarity"] = df.embedding_vec.apply(lambda x: cls.cosine_similarity(x, product_embedding))

        results = (
            df.sort_values("similarity", ascending=False)
            .head(n)
            .combined.str.replace("Title: ", "")
            .str.replace("; Content:", ": ")
        )
        if pprint:
            for r in results:
                print(r[:200])
                print()
        return results


if __name__ == "__main__":
    # 向量化,会消耗token
    # Embedding.create_embedding()
    # Embedding.search_by_embedding("dog food")
    Embedding.search_by_embedding("dog food")
