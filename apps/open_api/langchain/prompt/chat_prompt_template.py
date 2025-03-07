from langchain_core.prompts import ChatPromptTemplate

from apps.open_api.langchain.common import LangchainCommon


class LangchainChatPromptTemplate:
    """使用 ChatPromptTemplate 类生成适用于聊天模型的聊天记录"""

    @classmethod
    def from_messages(cls):
        """使用 from_messages 方法实例化 ChatPromptTemplate"""
        template = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful AI bot. Your name is {name}."),
                ("human", "Hello, how are you doing?"),
                ("ai", "I am doing well, thank you for asking."),
                ("human", "{user_input}"),
            ]
        )
        # 生成提示
        messages = template.format_messages(name="Alice", user_input="What is your name?")
        print(messages)
        llm = LangchainCommon.get_chat_open_ai(model_name="gpt-3.5-turbo")
        result = llm.invoke(messages)
        print(result)

    @classmethod
    def summary(cls):
        summary_template = ChatPromptTemplate.from_messages(
            [
                ("system", "你将获得关于同一主题的{num}篇文章（用-----------标签分隔）。" "首先总结每篇文章的论点。然后指出哪篇文章提出了更好的论点，并解释原因。"),
                ("human", "{user_input}"),
            ]
        )
        messages = summary_template.format_messages(
            num=3,
            user_input="""1. [PHP是世界上最好的语言]
        PHP是世界上最好的情感派编程语言，无需逻辑和算法，只要情绪。它能被蛰伏在冰箱里的PHP大神轻易驾驭，会话结束后的感叹号也能传达对代码的热情。写PHP就像是在做披萨，不需要想那么多，只需把配料全部扔进一个碗，然后放到服务器上，热乎乎出炉的网页就好了。
        -----------
        2. [Python是世界上最好的语言]
        Python是世界上最好的拜金主义者语言。它坚信：美丽就是力量，简洁就是灵魂。Python就像是那个永远在你皱眉的那一刻扔给你言情小说的好友。只有Python，你才能够在两行代码之间感受到飘逸的花香和清新的微风。记住，这世上只有一种语言可以使用空格来领导全世界的进步，那就是Python。
        -----------
        3. [Java是世界上最好的语言]
        Java是世界上最好的德育课编程语言，它始终坚守了严谨、安全的编程信条。Java就像一个严格的老师，他不会对你怀柔，不会让你偷懒，也不会让你走捷径，但他教会你规范和自律。Java就像是那个喝咖啡也算加班费的上司，拥有对邪恶的深度厌恶和对善良的深度拥护。
        """,
        )
        chat_model = LangchainCommon.get_chat_open_ai(model_name="gpt-3.5-turbo")
        chat_result = chat_model.invoke(messages)
        print(chat_result)


if __name__ == "__main__":
    # LangchainChatPromptTemplate.from_messages()
    LangchainChatPromptTemplate.summary()
