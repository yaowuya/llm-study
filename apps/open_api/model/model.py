from pprint import pprint

from openai import OpenAI

from core.settings import settings

OPEN_API_CLIENT = OpenAI(api_key=settings.open_api_key)

"""
使用 Models API 查看和访问 OpenAI 提供的预训练大语言模型
"""


class OpenAIModel:
    @classmethod
    def list_model(cls):
        """列出当前可用的模型，并提供每个模型的基本信息，如所有者和可用性。"""
        models = OPEN_API_CLIENT.models.list()
        print(models.data)
        print(OPEN_API_CLIENT.models.retrieve("gpt-4.5-preview"))

    @classmethod
    def test_completion(cls):
        """测试文本内容补全"""
        data = OPEN_API_CLIENT.completions.create(
            model="gpt-3.5-turbo-instruct", prompt="Say this is a test", max_tokens=7, temperature=0
        )
        print(data)
        text = data.choices[0].text
        print(text)

    @classmethod
    def create_completions(
        cls, prompt: str = "", model: str = "gpt-3.5-turbo-instruct", max_tokens: int = 1000, temperature: float = 0
    ):
        """创建文本内容补全"""
        data = OPEN_API_CLIENT.completions.create(
            model=model, prompt=prompt, max_tokens=max_tokens, temperature=temperature
        )
        print(data)
        return data.choices[0].text

    @classmethod
    def test_create_chat_completions(cls):
        """创建对话文本内容补全"""
        messages = [{"role": "user", "content": "Hello!"}]
        data = OPEN_API_CLIENT.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        print(data)
        # 从返回的数据中获取生成的消息
        new_message = data.choices[0].message
        # 打印 new_message
        print(new_message)
        new_message_dict = {"role": new_message.role, "content": new_message.content}
        print(new_message_dict)
        # 将消息追加到 messages 列表中
        messages.append(new_message_dict)
        print(messages)
        new_chat = {"role": "user", "content": "1.讲一个程序员才听得懂的冷笑话；2.今天是几号？3.明天星期几？"}
        messages.append(new_chat)
        pprint(messages)
        data = OPEN_API_CLIENT.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        new_message = data.choices[0].message
        # 打印 new_messages
        print(new_message)
        # 打印 new_messages 内容
        print(new_message.content)

    @classmethod
    def multi_role_chat(cls):
        """目前role参数支持3类身份： system, user assistant"""
        messages = [{"role": "system", "content": "你是一个乐于助人的体育界专家"}, {"role": "user", "content": "2008年奥运会是在哪里举行的？"}]
        data = OPEN_API_CLIENT.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        message = data.choices[0].message.content
        print(f"第一轮对话返回：\n{message}")
        # 添加 GPT 返回结果到聊天记录
        messages.append({"role": "assistant", "content": message})
        print(f"聊天结果添加到聊天记录中：\n{messages}")
        # 第二轮对话
        messages.append({"role": "user", "content": "1.金牌最多的是哪个国家？2.奖牌最多的是哪个国家？"})
        data = OPEN_API_CLIENT.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        message = data.choices[0].message.content
        print(f"第一轮对话返回：\n{message}")


if __name__ == "__main__":
    # OpenAIModel.list_model()
    # OpenAIModel.test_completion()
    # 测试对话
    # text = OpenAIModel.create_completions(
    #     prompt="讲10个给程序员听得笑话",
    #     temperature=0.5
    # )

    # 代码生成
    # text = OpenAIModel.create_completions(
    #     prompt="生成可执行的快速排序 Python 代码,要求代码简洁高效",
    #     temperature=0
    # )
    # print(text)

    # OpenAIModel.test_create_chat_completions()
    OpenAIModel.multi_role_chat()
