from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

from apps.open_api.langchain.common import LangchainCommon


class LangChainFewShotPrompt:
    """Few-shot Prompt 是一种通过提供少量示例（通常在 2-10 个之间）来引导大语言模型（LLM）生成所需结果的方法"""

    @classmethod
    def get_example_prompt(cls):
        """获取示例 Few-shot Prompt"""
        examples = [
            {
                "question": "谁活得更久，穆罕默德·阿里还是艾伦·图灵？",
                "answer": """
                    这里需要进一步的问题吗：是的。
                    追问：穆罕默德·阿里去世时多大了？
                    中间答案：穆罕默德·阿里去世时74岁。
                    追问：艾伦·图灵去世时多大了？
                    中间答案：艾伦·图灵去世时41岁。
                    所以最终答案是：穆罕默德·阿里
                    """,
            },
            {
                "question": "craigslist的创始人是什么时候出生的？",
                "answer": """
                    这里需要进一步的问题吗：是的。
                    追问：谁是craigslist的创始人？
                    中间答案：Craigslist是由Craig Newmark创办的。
                    追问：Craig Newmark是什么时候出生的？
                    中间答案：Craig Newmark出生于1952年12月6日。
                    所以最终答案是：1952年12月6日
                    """,
            },
            {
                "question": "乔治·华盛顿的外祖父是谁？",
                "answer": """
                    这里需要进一步的问题吗：是的。
                    追问：谁是乔治·华盛顿的母亲？
                    中间答案：乔治·华盛顿的母亲是Mary Ball Washington。
                    追问：Mary Ball Washington的父亲是谁？
                    中间答案：Mary Ball Washington的父亲是Joseph Ball。
                    所以最终答案是：Joseph Ball
                    """,
            },
            {
                "question": "《大白鲨》和《皇家赌场》的导演是同一个国家的吗？",
                "answer": """
                    这里需要进一步的问题吗：是的。
                    追问：谁是《大白鲨》的导演？
                    中间答案：《大白鲨》的导演是Steven Spielberg。
                    追问：Steven Spielberg来自哪里？
                    中间答案：美国。
                    追问：谁是《皇家赌场》的导演？
                    中间答案：《皇家赌场》的导演是Martin Campbell。
                    追问：Martin Campbell来自哪里？
                    中间答案：新西兰。
                    所以最终答案是：不是
                    """,
            },
        ]
        example_prompt = PromptTemplate(
            input_variables=["question", "answer"], template="Question:{question}\n{answer}"
        )
        # print(example_prompt.format(**examples[0]))
        return examples, example_prompt

    @classmethod
    def few_shot_prompt(cls):
        examples, example_prompt = cls.get_example_prompt()
        few_shot_prompt = FewShotPromptTemplate(
            examples=examples,  # 使用前面定义的 examples 作为范例
            example_prompt=example_prompt,  # 使用前面定义的 example_prompt 作为提示模板
            suffix="Question: {input}",  # 后缀模板，其中 {input} 会被替换为实际输入
            input_variables=["input"],  # 定义输入变量的列表
        )
        # 使用给定的输入格式化 prompt，并打印结果
        # 这里的 {input} 将被 "玛丽·波尔·华盛顿的父亲是谁?" 替换
        # print(few_shot_prompt.format(input="玛丽·波尔·华盛顿的父亲是谁?"))
        llm = LangchainCommon.get_open_ai(model_name="gpt-3.5-turbo-instruct", max_tokens=1000)
        result = llm.invoke(few_shot_prompt.format(input="华为的创始人是什么时候出生的？"))
        print(result)


if __name__ == "__main__":
    # LangChainFewShotPrompt.get_example_prompt()
    LangChainFewShotPrompt.few_shot_prompt()
