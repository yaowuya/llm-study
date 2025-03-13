# 使用 LangChain 构建一个 RAG 应用

## RAG 是什么

RAG 是一种将检索到的文档上下文与大语言模型（LLM）结合起来生成答案的技术。

整个过程主要分为以下几个步骤：

1. 加载文档：将原始数据(来源可能是在线网站、本地文件、各类平台等)加载到 LangChain 中。
2. 文档分割：将加载的文档分割成较小的块，以适应模型的上下文窗口，并更容易进行向量嵌入和检索。
3. 存储嵌入：将分割后的文档内容嵌入到向量空间，并存储到向量数据库中，以便后续检索。
4. 检索文档：通过查询向量数据库，检索与问题最相关的文档片段。
5. 生成回答：将检索到的文档片段与用户问题组合，生成并返回答案。

通过这些步骤，可以构建一个强大的问答系统，将复杂任务分解为更小的步骤并生成详细回答。

![rag](../../asserts/images/rag.png)

```
# 去掉pip install 使用项目依赖版本
# !pip install langchain langchain_community langchain_chroma
```


## **RAG 开发指南**

**本指南将详细介绍如何使用 LangChain 框架构建一个基于检索增强生成 (RAG) 的应用。**

下面是基于 LangChain 实现的 RAG 的核心步骤与使用到的关键代码抽象（类型、方法、库等）:

1. **加载文档**: 使用 `WebBaseLoader` 类从指定来源加载内容，并生成 `Document` 对象（依赖 `bs4` 库）。
2. **文档分割**: 使用 `RecursiveCharacterTextSplitter` 类的 `split_documents()` 方法将长文档分割成较小的块。
3. **存储嵌入**: 使用 `Chroma` 类的 `from_documents()` 方法将分割后的文档内容嵌入向量空间，并存储在向量数据库中（使用 `OpenAIEmbeddings`），并可以通过检查存储的向量数量来确认存储成功。。
4. **检索文档**: 使用 `VectorStoreRetriever` 类的 `as_retriever()` 和 `invoke()` 方法基于查询从向量数据库中检索最相关的文档片段。
5. **生成回答**: 使用 `ChatOpenAI` 类的 `invoke()` 方法，将检索到的文档片段与用户问题结合，生成回答（通过 `RunnablePassthrough` 和 `StrOutputParser`）。

我们使用的文档是Lilian Weng撰写的《LLM Powered Autonomous Agents》博客文章（[https://lilianweng.github.io/posts/2023-06-23-agent/](https://lilianweng.github.io/posts/2023-06-23-agent/) ），最终构建好的 RAG 应用支持我们询问关于该文章内容的相关问题。




#### ⭐️**LCEL 在 RAG 中的应用**⭐️

##### **LCEL 概述**

LCEL 是 LangChain 中的一个重要概念，它提供了一种统一的接口，允许不同的组件（如 `retriever`, `prompt`, `llm` 等）可以通过统一的 `Runnable` 接口连接起来。每个 `Runnable` 组件都实现了相同的方法，如 `.invoke()`、`.stream()` 或 `.batch()`，这使得它们可以通过 `|` 操作符轻松连接。

##### **LCEL 中处理的组件**

* **Retriever**: 负责根据用户问题检索相关文档。
* **Prompt**: 根据检索到的文档构建提示，供模型生成回答。
* **LLM**: 接收提示并生成最终的回答。
* **StrOutputParser**: 解析 LLM 的输出，只提取字符串内容，供最终显示。

##### **LCEL 运作机制**

* **构建链条**: 通过 `|` 操作符，我们可以将多个 `Runnable` 组件连接成一个 `RunnableSequence`。LangChain 会自动将一些对象转换为 `Runnable`，如将 `format_docs` 转换为 `RunnableLambda`，将包含 `"context"` 和 `"question"` 键的字典转换为 `RunnableParallel`。
* **数据流动**: 用户输入的问题会在 `RunnableSequence` 中依次经过各个 `Runnable` 组件。首先，问题会通过 `retriever` 检索相关文档，然后通过 `format_docs` 将这些文档转换为字符串。`RunnablePassthrough` 则直接传递原始问题。最后，这些数据被传递给 `prompt` 来生成完整的提示，供 LLM 使用。

##### **LCEL 中的关键操作**

* **格式化文档**: `retriever | format_docs` 将问题传递给 `retriever` 生成文档对象，然后通过 `format_docs` 将这些文档格式化为字符串。
* **传递问题**: `RunnablePassthrough()` 直接传递原始问题，保持原样。
* **构建提示**: `{"context": retriever | format_docs, "question": RunnablePassthrough()} | prompt` 构建完整的提示。
* **运行模型**: `prompt | llm | StrOutputParser()` 运行 LLM 生成回答，并解析输出。
