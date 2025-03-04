import pandas as pd


class Embedding:

    @classmethod
    def load_data(cls):
        input_datapath = "./apps/open_api/data/fine_food_reviews_1k.csv"
        df = pd.read_csv(input_datapath, index_col=0)
        df = df[["Time", "ProductId", "UserId", "Score", "Summary", "Text"]]
        df = df.dropna()

        # 将 "Summary" 和 "Text" 字段组合成新的字段 "combined"
        df["combined"] = (
                "Title: " + df.Summary.str.strip() + "; Content: " + df.Text.str.strip()
        )
        # print(df.head(2))
        # print(df["combined"])

    @classmethod
    def create_embedding(cls):
        # 模型类型
        # 建议使用官方推荐的第二代嵌入模型：text-embedding-ada-002
        embedding_model = "text-embedding-ada-002"
        # text-embedding-ada-002 模型对应的分词器（TOKENIZER）
        embedding_encoding = "cl100k_base"
        # text-embedding-ada-002 模型支持的输入最大 Token 数是8191，向量维度 1536
        # 在我们的 DEMO 中过滤 Token 超过 8000 的文本
        max_tokens = 8000
        print(embedding_model, embedding_encoding, max_tokens)


if __name__ == "__main__":
    Embedding.load_data()
