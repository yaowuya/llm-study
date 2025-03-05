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


if __name__ == "__main__":
    OpenAIModel.list_model()
