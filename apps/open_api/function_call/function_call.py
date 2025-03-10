import requests
from tenacity import retry, stop_after_attempt, wait_random_exponential
from termcolor import colored

from core.settings import settings


class FunctionCall:
    @classmethod
    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def chat_completion_request(cls, messages, functions=None, function_call=None, model="gpt-3.5-turbo"):
        """创建对话文本内容补全
        # 使用了retry库，指定在请求失败时的重试策略。
        # 这里设定的是指数等待（wait_random_exponential），时间间隔的最大值为40秒，并且最多重试3次（stop_after_attempt(3)）。
        # 定义一个函数chat_completion_request，主要用于发送 聊天补全 请求到OpenAI服务器
        """
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {settings.open_api_key}"}
        json_data = {"model_io": model, "messages": messages}
        if functions is not None:
            json_data["functions"] = functions
        if function_call is not None:
            json_data["function_call"] = function_call
        try:
            open_api_url = "https://api.openai.com/v1/chat/completions"
            response = requests.post(
                open_api_url,
                headers=headers,
                json=json_data,
            )
            return response
        except Exception as e:
            print(f"exception: {e}")
            return e

    @staticmethod
    def pretty_print_conversation(messages):
        # 定义一个函数pretty_print_conversation，用于打印消息对话内容
        # 为不同角色设置不同的颜色
        role_to_color = {
            "system": "red",
            "user": "green",
            "assistant": "blue",
            "function": "magenta",
        }

        # 遍历消息列表
        for message in messages:

            # 如果消息的角色是"system"，则用红色打印“content”
            if message["role"] == "system":
                print(colored(f"system: {message['content']}\n", role_to_color[message["role"]]))

            # 如果消息的角色是"user"，则用绿色打印“content”
            elif message["role"] == "user":
                print(colored(f"user: {message['content']}\n", role_to_color[message["role"]]))

            # 如果消息的角色是"assistant"，并且消息中包含"function_call"，则用蓝色打印"function_call"
            elif message["role"] == "assistant" and message.get("function_call"):
                print(
                    colored(f"assistant[function_call]: {message['function_call']}\n", role_to_color[message["role"]])
                )

            # 如果消息的角色是"assistant"，但是消息中不包含"function_call"，则用蓝色打印“content”
            elif message["role"] == "assistant" and not message.get("function_call"):
                print(colored(f"assistant[content]: {message['content']}\n", role_to_color[message["role"]]))

            # 如果消息的角色是"function"，则用品红色打印“function”
            elif message["role"] == "function":
                print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))

    @classmethod
    def test_not_sure_location(cls, funcs):
        # 定义一个空列表messages，用于存储聊天的内容
        messages = []
        # 使用append方法向messages列表添加一条系统角色的消息
        messages.append(
            {
                "role": "system",  # 消息的角色是"system"
                "content": "Don't make assumptions about what values to plug into functions. "
                "Ask for clarification if a user request is ambiguous.",  # 消息的内容
            }
        )
        # 向messages列表添加一条用户角色的消息
        messages.append({"role": "user", "content": "What's the weather like today"})  # 消息的角色是"user"  # 用户询问今天的天气情况
        # 使用定义的chat_completion_request函数发起一个请求，传入messages和functions作为参数
        chat_response = cls.chat_completion_request(messages, functions=funcs)
        # 解析返回的JSON数据，获取助手的回复消息
        assistant_message = chat_response.json()["choices"][0]["message"]
        # 将助手的回复消息添加到messages列表中
        messages.append(assistant_message)
        cls.pretty_print_conversation(messages)
        return messages

    @classmethod
    def test_sure_location(cls, funcs, messages: list):
        # 向messages列表添加一条用户角色的消息，用户告知他们在苏格兰的格拉斯哥
        messages.append({"role": "user", "content": "I'm in Shanghai, China."})  # 消息的角色是"user"  # 用户的消息内容

        # 再次使用定义的chat_completion_request函数发起一个请求，传入更新后的messages和functions作为参数
        chat_response = cls.chat_completion_request(messages, functions=funcs)
        # 解析返回的JSON数据，获取助手的新的回复消息
        assistant_message = chat_response.json()["choices"][0]["message"]
        # 将助手的新的回复消息添加到messages列表中
        messages.append(assistant_message)
        cls.pretty_print_conversation(messages)
        return messages


if __name__ == "__main__":
    # 定义一个名为functions的列表，其中包含两个字典，这两个字典分别定义了两个功能的相关参数

    # 第一个字典定义了一个名为"get_current_weather"的功能
    functions = [
        {
            "name": "get_current_weather",  # 功能的名称
            "description": "Get the current weather",  # 功能的描述
            "parameters": {  # 定义该功能需要的参数
                "type": "object",
                "properties": {  # 参数的属性
                    "location": {  # 地点参数
                        "type": "string",  # 参数类型为字符串
                        "description": "The city and state, e.g. San Francisco, CA",  # 参数的描述
                    },
                    "format": {  # 温度单位参数
                        "type": "string",  # 参数类型为字符串
                        "enum": ["celsius", "fahrenheit"],  # 参数的取值范围
                        "description": "The temperature unit to use. Infer this from the users location.",  # 参数的描述
                    },
                },
                "required": ["location", "format"],  # 该功能需要的必要参数
            },
        },
        # 第二个字典定义了一个名为"get_n_day_weather_forecast"的功能
        {
            "name": "get_n_day_weather_forecast",  # 功能的名称
            "description": "Get an N-day weather forecast",  # 功能的描述
            "parameters": {  # 定义该功能需要的参数
                "type": "object",
                "properties": {  # 参数的属性
                    "location": {  # 地点参数
                        "type": "string",  # 参数类型为字符串
                        "description": "The city and state, e.g. San Francisco, CA",  # 参数的描述
                    },
                    "format": {  # 温度单位参数
                        "type": "string",  # 参数类型为字符串
                        "enum": ["celsius", "fahrenheit"],  # 参数的取值范围
                        "description": "The temperature unit to use. Infer this from the users location.",  # 参数的描述
                    },
                    "num_days": {  # 预测天数参数
                        "type": "integer",  # 参数类型为整数
                        "description": "The number of days to forecast",  # 参数的描述
                    },
                },
                "required": ["location", "format", "num_days"],  # 该功能需要的必要参数
            },
        },
    ]
    messages = FunctionCall.test_not_sure_location(functions)
    print(messages)
    messages = FunctionCall.test_sure_location(functions, messages)
    print(messages)
