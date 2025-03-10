from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SequentialChain, SimpleSequentialChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from apps.open_api.langchain.common import LangchainCommon


class SequentialChainService:
    """串联式调用语言模型（将一个调用的输出作为另一个调用的输入）。"""

    def __init__(self):
        self.llm = LangchainCommon.get_chat_open_ai(model_name="gpt-4o-mini", temperature=0.9, max_tokens=1000)

    def origin_chain(self):
        prompt = PromptTemplate(input_variables=["product"], template="给制造{product}的有限公司取10个好名字，并给出完整的公司名称")
        chain = LLMChain(llm=self.llm, prompt=prompt, verbose=True)
        print(chain.invoke({"product": "性能卓越的GPU"}))

    def simple_sequence_chain(self):
        synopsis_template = """你是一位剧作家。根据戏剧的标题，你的任务是为该标题写一个简介。

        标题：{title}
        剧作家：以下是对上述戏剧的简介："""
        synopsis_prompt_template = PromptTemplate(input_variables=["title"], template=synopsis_template)
        synopsis_chain = LLMChain(llm=self.llm, prompt=synopsis_prompt_template, verbose=True)

        # 这是一个LLMChain，用于根据剧情简介撰写一篇戏剧评论。
        # llm = OpenAI(temperature=0.7, max_tokens=1000)
        review_template = """你是《纽约时报》的戏剧评论家。根据剧情简介，你的工作是为该剧撰写一篇评论。

        剧情简介：
        {synopsis}

        以下是来自《纽约时报》戏剧评论家对上述剧目的评论："""
        review_prompt_template = PromptTemplate(input_variables=["synopsis"], template=review_template)
        review_chain = LLMChain(llm=self.llm, prompt=review_prompt_template, verbose=True)
        # 这是一个SimpleSequentialChain，按顺序运行这两个链
        overall_chain = SimpleSequentialChain(chains=[synopsis_chain, review_chain], verbose=True)
        review = overall_chain.invoke("星球大战第九季")
        print(review)

    def sequential_chain(self):
        """使用 SequentialChain 实现戏剧摘要和评论（多输入/多输出）"""
        synopsis_template = """你是一位剧作家。根据戏剧的标题和设定的时代，你的任务是为该标题写一个简介。

        标题：{title}
        时代：{era}
        剧作家：以下是对上述戏剧的简介："""

        synopsis_prompt_template = PromptTemplate(input_variables=["title", "era"], template=synopsis_template)
        # output_key
        synopsis_chain = LLMChain(llm=self.llm, prompt=synopsis_prompt_template, output_key="synopsis", verbose=True)
        # 这是一个LLMChain，用于根据剧情简介撰写一篇戏剧评论。
        review_template = """你是《纽约时报》的戏剧评论家。根据该剧的剧情简介，你需要撰写一篇关于该剧的评论。

        剧情简介：
        {synopsis}

        来自《纽约时报》戏剧评论家对上述剧目的评价："""

        review_prompt_template = PromptTemplate(input_variables=["synopsis"], template=review_template)
        review_chain = LLMChain(llm=self.llm, prompt=review_prompt_template, output_key="review", verbose=True)
        m_overall_chain = SequentialChain(
            chains=[synopsis_chain, review_chain],
            input_variables=["title", "era"],
            output_variables=["synopsis", "review"],  # 定义返回的键名
            verbose=True,
        )
        m_overall_chain.invoke({"title": "三体人不是无法战胜的", "era": "二十一世纪的新中国"})

    def runnable_sequence(self):
        # The class `LLMChain` was deprecated in LangChain 0.1.17 and will be removed in 1.0.
        # Use :meth:`~RunnableSequence, e.g., `prompt | llm`` instead.
        # 【新增】langchain 0.3版本，使用RunnableSequence替换LLMChain，并指定 output_key
        summarizing_prompt_template = """
        总结以下文本为一个 20 字以内的句子:
        ---
        {content}
        """
        summarizing_prompt = PromptTemplate.from_template(summarizing_prompt_template)
        summarizing_chain = summarizing_prompt | self.llm | StrOutputParser()

        translating_prompt_template = """
        将{summary}翻译成英文:
        """
        translating_prompt = PromptTemplate.from_template(translating_prompt_template)
        translating_chain = translating_prompt | self.llm | StrOutputParser()

        # Construct a RunnableSequence with custom output keys
        overall_chain = summarizing_chain | {"summary": summarizing_chain, "translation": translating_chain}
        test_content = """
        端到端在深度学习中指的是一种模型架构设计理念：
        从原始输入数据到最终输出结果，整个决策过程完全由单一神经网络完成，无需人工设计中间处理环节。
        这种设计摒弃了传统分步骤、模块化的处理流程，让模型自主挖掘数据中隐藏的复杂关联。
        """
        result = overall_chain.invoke({"content": test_content})
        print(result)


if __name__ == "__main__":
    sc = SequentialChainService()
    # sc.origin_chain()
    # sc.simple_sequence_chain()
    # sc.sequential_chain()
    sc.runnable_sequence()
