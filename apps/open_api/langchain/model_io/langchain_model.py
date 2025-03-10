from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAI

from core.settings import settings


class LangchainModel:
    def __init__(self, model_name: str = "gpt-3.5-turbo-instruct", temperature: float = 0.7):
        self.open_api = OpenAI(
            model_name=model_name, openai_api_key=settings.open_api_key, max_tokens=1024, temperature=temperature
        )
        self.chat_model = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=settings.open_api_key)

    def test_simple_model(self, message: str):
        print(self.open_api.invoke(message))

    def test_chat_model(self):
        message = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="Who won the world series in 2020?"),
            AIMessage(content="The Los Angeles Dodgers won the World Series in 2020."),
            HumanMessage(content="Where was it played?"),
        ]
        chat_result = self.chat_model.invoke(message)
        print(chat_result)


if __name__ == "__main__":
    langchain_model = LangchainModel()
    # langchain_model.test_simple_model("讲10个给程序员听得笑话")
    langchain_model.test_chat_model()
