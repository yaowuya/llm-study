from langchain_core.prompts import PromptTemplate

from apps.open_api.langchain.common import LangchainCommon


class LangchainPromptTemplate:
    """使用 PromptTemplate 类生成提升词"""

    @classmethod
    def prompt_format(cls):
        """使用 from_template 方法实例化 PromptTemplate"""
        prompt_template = PromptTemplate.from_template("Tell me a {adjective} joke about {content}.")

        # 使用 format 生成提示
        prompt = prompt_template.format(adjective="funny", content="chickens")
        print(prompt)

    @classmethod
    def prompt_initializer(cls):
        """使用构造函数（Initializer）实例化 PromptTemplate"""
        valid_prompt = PromptTemplate(
            input_variables=["adjective", "content"], template="Tell me a {adjective} joke about {content}."
        )
        print(valid_prompt)
        print(valid_prompt.format(adjective="funny", content="chickens"))

    @classmethod
    def prompt_invoke(cls):
        prompt_template = PromptTemplate(input_variables=["num"], template="讲{num}个给程序员听得笑话")
        llm = LangchainCommon.get_open_ai(model_name="gpt-3.5-turbo-instruct", max_tokens=1000)
        prompt = prompt_template.format(num=2)
        print(f"Prompt: {prompt}")
        result = llm.invoke(prompt)
        print(f"result: {result}")

    @classmethod
    def prompt_jinja2(cls):
        """使用 jinja2 生成模板化提示"""
        jinja2_template = "Tell me a {{ adjective }} joke about {{ content }}"
        prompt = PromptTemplate.from_template(jinja2_template, template_format="jinja2")
        prompt.format(adjective="funny", content="chickens")
        print(prompt)

    @classmethod
    def prompt_multi_language_code(cls, programming_language: str = "Python"):
        """实测：生成多种编程语言版本的快速排序"""
        sort_prompt_template = PromptTemplate.from_template("生成可执行的快速排序{programming_language}代码")
        llm = LangchainCommon.get_open_ai(model_name="gpt-3.5-turbo-instruct", max_tokens=1000)
        result = llm.invoke(sort_prompt_template.format(programming_language=programming_language))
        print(result)


if __name__ == "__main__":
    # LangchainPromptTemplate.prompt_format()
    # LangchainPromptTemplate.prompt_initializer()
    # LangchainPromptTemplate.prompt_invoke()
    # LangchainPromptTemplate.prompt_multi_language_code("python")
    LangchainPromptTemplate.prompt_multi_language_code("java")
