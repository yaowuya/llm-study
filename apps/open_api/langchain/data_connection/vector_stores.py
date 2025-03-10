from langchain.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain.vectorstores import Chroma

from core.settings import settings


class VectorStores:

    def chroma_example(self):
        # 加载长文本
        raw_documents = TextLoader('./apps/open_api/data/state_of_the_union.txt', encoding='utf-8').load()
        # 实例化文本分割器
        text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0)
        # 分割文本
        documents = text_splitter.split_documents(raw_documents)
        embeddings_model = OpenAIEmbeddings(openai_api_key=settings.open_api_key)
        # 将分割后的文本，使用 OpenAI 嵌入模型获取嵌入向量，并存储在 Chroma 中
        db = Chroma.from_documents(documents, embeddings_model)
        # 使用文本进行语义相似度搜索
        query = "What did the president say about Ketanji Brown Jackson"
        docs = db.similarity_search(query)
        print(docs[0].page_content)

        # 使用嵌入向量进行语义相似度搜索
        embedding_vector = embeddings_model.embed_query(query)
        docs = db.similarity_search_by_vector(embedding_vector)
        print(docs[0].page_content)


if __name__ == '__main__':
    vector_stores = VectorStores()
    vector_stores.chroma_example()
