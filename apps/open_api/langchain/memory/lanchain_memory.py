from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory

from apps.open_api.langchain.common import LangchainCommon


class LangchainMemory:
    def __init__(self):
        self.llm = LangchainCommon.get_open_ai(temperature=0, max_tokens=2000)

    def conversation(self):
        conversation = ConversationChain(llm=self.llm, verbose=True, memory=ConversationBufferMemory())
        conversation.predict(input="你好呀！")
        print(conversation.predict(input="你为什么叫小米？跟雷军有关系吗？"))

    def conversation_buffer_window_memory(self):
        """
        ConversationBufferWindowMemory 会在时间轴上保留对话的交互列表。
        它只使用最后 K 次交互。这对于保持最近交互的滑动窗口非常有用，以避免缓冲区过大。
        """
        conversation_with_summary = ConversationChain(
            llm=self.llm,
            # We set a low k=2, to only keep the last 2 interactions in memory
            memory=ConversationBufferWindowMemory(k=2),
            verbose=True,
        )
        conversation_with_summary.predict(input="嗨，你最近过得怎么样？")
        conversation_with_summary.predict(input="你最近学到什么新知识了?")
        conversation_with_summary.predict(input="展开讲讲？")
        conversation_with_summary.predict(input="如果要构建聊天机器人，具体要用什么自然语言处理技术?")


if __name__ == "__main__":
    # LangchainMemory().conversation()
    LangchainMemory().conversation_buffer_window_memory()
