from langchain.chains.conversation.base import ConversationChain
from langchain.chains.llm import LLMChain
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain_core.prompts import PromptTemplate

from apps.open_api.langchain.common import LangchainCommon


class RouterChainService:
    """使用 LLMRouterChain 实现条件判断调用"""

    def __init__(self):
        self.llm = LangchainCommon.get_open_ai()

    def router_chain(self):
        physics_template = """你是一位非常聪明的物理教授。
        你擅长以简洁易懂的方式回答关于物理的问题。
        当你不知道某个问题的答案时，你会坦诚承认。

        这是一个问题：
        {input}"""

        math_template = """你是一位很棒的数学家。你擅长回答数学问题。
        之所以如此出色，是因为你能够将难题分解成各个组成部分，
        先回答这些组成部分，然后再将它们整合起来回答更广泛的问题。

        这是一个问题：
        {input}"""

        prompt_infos = [
            {
                "name": "物理",
                "description": "适用于回答物理问题",
                "prompt_template": physics_template,
            },
            {
                "name": "数学",
                "description": "适用于回答数学问题",
                "prompt_template": math_template,
            },
        ]

        # 创建一个空的目标链字典，用于存放根据prompt_infos生成的LLMChain。
        destination_chains = {}

        # 遍历prompt_infos列表，为每个信息创建一个LLMChain。
        for p_info in prompt_infos:
            name = p_info["name"]  # 提取名称
            prompt_template = p_info["prompt_template"]  # 提取模板
            # 创建PromptTemplate对象
            prompt = PromptTemplate(template=prompt_template, input_variables=["input"])
            # 使用上述模板和llm对象创建LLMChain对象
            chain = LLMChain(llm=self.llm, prompt=prompt)
            # 将新创建的chain对象添加到destination_chains字典中
            destination_chains[name] = chain

        # 创建一个默认的ConversationChain
        default_chain = ConversationChain(llm=self.llm, output_key="text")

        # 这段代码定义了一个chain对象（LLMRouterChain），该对象首先使用router_chain来决定哪个destination_chain应该被执行，
        # 如果没有合适的目标链，则默认使用default_chain。
        # 从prompt_infos中提取目标信息并将其转化为字符串列表
        destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
        # 使用join方法将列表转化为字符串，每个元素之间用换行符分隔
        destinations_str = "\n".join(destinations)
        # 根据MULTI_PROMPT_ROUTER_TEMPLATE格式化字符串和destinations_str创建路由模板
        router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations_str)
        # 创建路由的PromptTemplate
        router_prompt = PromptTemplate(
            template=router_template,
            input_variables=["input"],
            output_parser=RouterOutputParser(),
        )
        # 使用上述路由模板和llm对象创建LLMRouterChain对象
        router_chain = LLMRouterChain.from_llm(self.llm, router_prompt)
        # 创建MultiPromptChain对象，其中包含了路由链，目标链和默认链。
        chain = MultiPromptChain(
            router_chain=router_chain,
            destination_chains=destination_chains,
            default_chain=default_chain,
            verbose=True,
        )
        print(chain.invoke("黑体辐射是什么？?"))
        print(chain.invoke("大于40的第一个质数是多少，使得这个质数加一能被3整除？"))


if __name__ == "__main__":
    router_chain_service = RouterChainService()
    router_chain_service.router_chain()
