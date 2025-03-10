from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SimpleSequentialChain
from langchain.chains.transform import TransformChain
from langchain_core.prompts import PromptTemplate

from apps.open_api.langchain.common import LangchainCommon


class TransformChainService:
    """Transform Chain: 实现快捷处理超长文本"""

    def __init__(self):
        self.llm = LangchainCommon.get_chat_open_ai(model_name="gpt-4o-mini", temperature=0.9, max_tokens=1000)

    @staticmethod
    def get_novel_text():
        with open("./apps/open_api/data/the_old_man_and_the_sea.txt", encoding="utf-8") as f:
            novel_text = f.read()
        return novel_text

    @staticmethod
    def transform_func(inputs: dict) -> dict:
        # 定义一个转换函数，输入是一个字典，输出也是一个字典。
        # 从输入字典中获取"text"键对应的文本。
        text = inputs["text"]
        # 使用split方法将文本按照"\n\n"分隔为多个段落，并只取前三个，然后再使用"\n\n"将其连接起来。
        shortened_text = "\n\n".join(text.split("\n\n")[:3])
        # 返回裁剪后的文本，用"output_text"作为键。
        return {"output_text": shortened_text}

    def transform_chain(self):
        # 使用上述转换函数创建一个TransformChain对象。
        # 定义输入变量为["text"]，输出变量为["output_text"]，并指定转换函数为transform_func。
        transform_chain = TransformChain(
            input_variables=["text"], output_variables=["output_text"], transform=self.transform_func
        )
        novel_text = self.get_novel_text()
        # transformed_novel = transform_chain.invoke(novel_text)
        # print(transformed_novel['text'])
        template = """总结下面文本:

        {output_text}

        总结:"""
        prompt = PromptTemplate(input_variables=["output_text"], template=template)
        llm_chain = LLMChain(llm=self.llm, prompt=prompt, verbose=True)
        sequential_chain = SimpleSequentialChain(chains=[transform_chain, llm_chain])
        summary = sequential_chain.invoke(novel_text[:1000])
        print(summary)


if __name__ == "__main__":
    transform_chain_service = TransformChainService()
    transform_chain_service.transform_chain()
