from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_openai import ChatOpenAI

from apps.sales_chatbot.faiss_service import FaissService
from core.settings import settings


class SalesChatbot:
    def __init__(self):
        self.faiss_service = FaissService()

    def initialize_faiss(self):
        """数据库向量化"""
        docs = self.faiss_service.load_and_split_data()
        self.faiss_service.embedding_and_save_data(docs)

    def get_faiss_db(self):
        """获取 Faiss DB"""
        return self.faiss_service.load_local_faiss()

    def retriever_search(self, db, query, top_k=3, score_threshold=0.8):
        """检索"""
        answer_list = self.faiss_service.retrieve_search(db, query, top_k=top_k, score_threshold=score_threshold)
        ans_list = [answer.page_content.split("[销售回答] ")[-1] for answer in answer_list]
        # print(ans_list)
        return ans_list

    def sale_chatbot(self, query, top_k=3, score_threshold=0.8):
        """销售机器人：当向量数据库中没有合适答案时，使用大语言模型能力"""
        db = self.get_faiss_db()
        retriever = self.faiss_service.retriever(db, top_k=top_k, score_threshold=score_threshold)
        llm = ChatOpenAI(model="gpt-4", openai_api_key=settings.open_api_key, temperature=0.5)
        qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)
        # 输出内部 Chain 的日志
        qa_chain.combine_documents_chain.verbose = True
        # 返回向量数据库的检索结果
        qa_chain.return_source_documents = True
        result = qa_chain({"query": query})
        return result


if __name__ == "__main__":
    chatbot = SalesChatbot()
    # 数据向量化
    # chatbot.initialize_faiss()
    # faiss_db = chatbot.get_faiss_db()
    # chatbot.retriever_search(faiss_db, "价格200万以内", score_threshold=0.6)
    result = chatbot.sale_chatbot("小区吵不吵")
    print(result)
