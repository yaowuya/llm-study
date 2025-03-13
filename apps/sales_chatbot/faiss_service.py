from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

from core.settings import settings


class FaissService:
    """Faiss 向量数据库：需要 CUDA 7.5+ 版本支持的 GPU"""

    def __init__(self):
        self.base_path = "./apps/sales_chatbot/data"
        self.data_path = f"{self.base_path}/real_estate_sales_data.txt"
        self.faiss_path = f"{self.base_path}/faiss_index"
        self.embeddings = OpenAIEmbeddings(openai_api_key=settings.open_api_key)

    def load_and_split_data(self):
        # 实例化文档加载器
        loader = TextLoader(self.data_path, encoding="utf-8")
        # 加载文档
        documents = loader.load()
        # 实例化文本分割器
        text_splitter = CharacterTextSplitter(
            separator=r"\d+\.",
            chunk_size=100,
            chunk_overlap=0,
            length_function=len,
            is_separator_regex=True,
        )
        # 分割文本
        docs = text_splitter.split_documents(documents)
        # print(docs)
        return docs

    def embedding_and_save_data(self, docs):
        # OpenAI Embedding 模型
        # FAISS 向量数据库，使用 docs 的向量作为初始化存储
        db = FAISS.from_documents(docs, self.embeddings)
        db.save_local(self.faiss_path)
        return db

    def load_local_faiss(self):
        """加载 Faiss DB"""
        new_db = FAISS.load_local(self.faiss_path, self.embeddings, allow_dangerous_deserialization=True)
        return new_db

    @classmethod
    def retriever(cls, db, top_k=3, score_threshold=0.8):
        """检索"""
        # 实例化一个 TopK Retriever
        # 使用 similarity_score_threshold 设置阈值，提升结果的相关性质量
        retriever = db.as_retriever(
            search_type="similarity_score_threshold", search_kwargs={"score_threshold": score_threshold, "k": top_k}
        )
        return retriever

    @classmethod
    def retrieve_search(cls, db, query, top_k=3, score_threshold=0.8):
        retriever = cls.retriever(db, top_k=top_k, score_threshold=score_threshold)
        answer_list = retriever.get_relevant_documents(query)
        return answer_list

    @classmethod
    def similarity_search(cls, db, query):
        answer_list = db.similarity_search(query)
        for answer in answer_list:
            print(answer.page_content)
        return answer_list
