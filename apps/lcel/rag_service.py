import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.settings import settings


class RagService:
    """RAG学习"""

    @classmethod
    def load_document(cls):
        """
        Step 1: 加载文档
            描述: 使用 DocumentLoader 从指定来源（如网页）加载内容，并将其转换为 Document 对象。
            重要代码抽象:
            类: WebBaseLoader
            方法: load()
            库: bs4 (BeautifulSoup)
            代码解释:
            文档加载: 使用 WebBaseLoader 从网页加载内容，并通过 BeautifulSoup 解析 HTML，提取重要的部分。
            检查加载数量: 打印加载的文档数量，确保所有文档正确加载。
            验证文档内容: 输出第一个文档的部分内容，确认加载的数据符合预期。
        """
        # 使用 WebBaseLoader 从网页加载内容，并仅保留标题、标题头和文章内容
        bs4_strainer = bs4.SoupStrainer(class_=("post-title", "post-header", "post-content"))
        loader = WebBaseLoader(
            web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
            bs_kwargs={"parse_only": bs4_strainer},
        )
        docs = loader.load()
        return docs

    @classmethod
    def splitter_text(cls, docs):
        """Step 2: 文档分割
        描述: 使用文本分割器将加载的长文档分割成较小的块，以便嵌入和检索。
        重要代码抽象:
        类: RecursiveCharacterTextSplitter
        方法: split_documents()
        代码解释:
        文档分割: 使用 RecursiveCharacterTextSplitter 按字符大小分割文档块，设置块大小和重叠字符数，确保文档块适合模型处理。
        检查块数量: 打印分割后的文档块数量，确保分割操作正确执行。
        验证块大小: 输出第一个块的字符数，确认分割块的大小是否符合预期。
        """
        # 使用 RecursiveCharacterTextSplitter 将文档分割成块，每块1000字符，重叠200字符
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
        all_splits = text_splitter.split_documents(docs)
        return all_splits

    @classmethod
    def embedding(cls, all_splits):
        """Step 3: 存储嵌入
        描述: 将分割后的文档内容嵌入到向量空间中，并存储到向量数据库，以便后续检索。
        重要代码抽象:
        类: Chroma
        方法: from_documents()
        类: OpenAIEmbeddings
        代码解释:
        存储嵌入: 使用 Chroma.from_documents() 方法将所有分割的文档片段进行嵌入(OpenAIEmbeddings嵌入模型)，将文档片段嵌入向量空间，并存储在向量数据库中。
        """
        # 使用 Chroma 向量存储和 OpenAIEmbeddings 模型，将分割的文档块嵌入并存储
        vectorstore = Chroma.from_documents(
            documents=all_splits,
            embedding=OpenAIEmbeddings(openai_api_key=settings.open_api_key),
        )
        # 查看 vectorstore 数据类型
        print(type(vectorstore))
        return vectorstore

    @classmethod
    def query_document(cls, vectorstore, query):
        """Step 4: 检索文档
        描述: 使用 VectorStoreRetriever 类的 as_retriever() 和 invoke() 方法，从向量数据库中检索与查询最相关的文档片段。
        重要代码抽象:
        类: VectorStoreRetriever
        方法: as_retriever(), invoke()
        代码解释:
        文档检索: 将向量存储转换为检索器，并基于查询执行相似性搜索，获取相关文档片段。
        检查检索数量: 打印检索到的文档片段数量，确保检索操作成功。
        验证检索内容: 输出第一个检索到的文档内容，确认检索结果与预期相符。
        在 LangChain 中，所有向量数据库都支持vectorstore.as_retriever 方法，实例化该数据库对应的检索器（Retriever），
        """
        # 使用 VectorStoreRetriever 从向量存储中检索与查询最相关的文档
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})
        retrieved_docs = retriever.invoke(query)
        return retrieved_docs

    @classmethod
    def generate_response(cls, query):
        """
        描述: 将之前构建的组件（检索器、提示、LLM等）组合成一个完整的链条，实现用户问题的检索与生成回答。
        完整链条：输入用户问题，检索相关文档，构建提示，
        将其传递给模型（使用ChatOpenAI 类的 invoke() 方法），并解析输出生成最终回答。
        重要代码抽象:
        类: ChatOpenAI
        方法: invoke()
        类: RunnablePassthrough
        类: StrOutputParser
        模块：hub
        代码解释:
        模型初始化: 使用 ChatOpenAI 类初始化一个 GPT-4o-mini 模型，准备处理生成任务。
        文档格式化: 定义 format_docs 函数，用于将检索到的文档内容格式化为字符串。
        构建 RAG 链: 使用 LCEL (LangChain Execution Layer) 的 | 操作符将各个组件连接成一个链条，
        包括文档检索、提示构建、模型调用以及输出解析。
        生成回答: 使用 stream() 方法逐步输出生成的回答，并实时展示，确保生成的结果符合预期。
        LangChain Hub
        LangChain Hub (https://smith.langchain.com/hub) 是一个提示词模板开源社区，为开发者提供了大量开箱即用的提示词模板。
        属于 LangSmith 产品的一部分。

        下面我们尝试使用 RAG 应用的提示词模板：https://smith.langchain.com/hub/rlm/rag-prompt
        """
        # 定义 RAG 链，将用户问题与检索到的文档结合并生成答案
        llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=settings.open_api_key)
        # 使用 hub 模块拉取 rag 提示词模板
        prompt = hub.pull("rlm/rag-prompt")
        docs = cls.load_document()
        all_splits = cls.splitter_text(docs)
        vectorstore = cls.embedding(all_splits)
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})
        # 使用 LCEL 构建 RAG Chain
        rag_chain = (
            {"context": retriever | cls.format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        # 流式生成回答
        for chunk in rag_chain.stream(query):
            print(chunk, end="", flush=True)

    @classmethod
    # 定义格式化文档的函数
    def format_docs(cls, docs):
        return "\n\n".join(doc.page_content for doc in docs)


if __name__ == "__main__":
    # 示例：从 https://lilianweng.github.io/posts/2023-06-23-agent/ 加载并检索文档
    RagService.generate_response("What is Task Decomposition?")
