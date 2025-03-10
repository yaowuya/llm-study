from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

from apps.open_api.langchain.common import LangchainCommon


class DocumentTransform:

    def __init__(self):
        self.llm = LangchainCommon.get_chat_open_ai()

    @staticmethod
    def get_long_text():
        # 加载待分割长文本
        with open('./apps/open_api/data/state_of_the_union.txt', encoding='utf-8') as f:
            state_of_the_union = f.read()
        return state_of_the_union

    def recursive_character_text_splitter(self):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=20,
            length_function=len,
            add_start_index=True
        )
        state_of_the_union = self.get_long_text()
        docs = text_splitter.create_documents([state_of_the_union])
        print(docs[0])
        print(docs[1])
        metadatas = [{"document": 1}, {"document": 2}]
        documents = text_splitter.create_documents([state_of_the_union, state_of_the_union], metadatas=metadatas)
        print(documents[0])

    def language_splitter(self):
        html_text = """
        <!DOCTYPE html>
        <html>
            <head>
                <title>🦜️🔗 LangChain</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                    }
                    h1 {
                        color: darkblue;
                    }
                </style>
            </head>
            <body>
                <div>
                    <h1>🦜️🔗 LangChain</h1>
                    <p>⚡ Building applications with LLMs through composability ⚡</p>
                </div>
                <div>
                    As an open source project in a rapidly developing field, we are extremely open to contributions.
                </div>
            </body>
        </html>
        """
        html_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.HTML, chunk_size=60, chunk_overlap=0
        )
        html_docs = html_splitter.create_documents([html_text])
        print(html_docs)


if __name__ == '__main__':
    document_transform = DocumentTransform()
    document_transform.recursive_character_text_splitter()
    document_transform.language_splitter()
