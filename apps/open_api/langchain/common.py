from langchain_openai import ChatOpenAI, OpenAI

from core.settings import settings


class LangchainCommon:
    @classmethod
    def get_open_ai(cls, model_name: str = "gpt-3.5-turbo-instruct", temperature: float = 0.7, max_tokens: int = 1024):
        open_ai = OpenAI(
            model=model_name, openai_api_key=settings.open_api_key, max_tokens=max_tokens, temperature=temperature
        )
        return open_ai

    @classmethod
    def get_chat_open_ai(
        cls, model_name: str = "gpt-3.5-turbo-instruct", temperature: float = 0.7, max_tokens: int = 1024
    ):
        chat_open_ai = ChatOpenAI(
            model=model_name, openai_api_key=settings.open_api_key, max_tokens=max_tokens, temperature=temperature
        )
        return chat_open_ai
