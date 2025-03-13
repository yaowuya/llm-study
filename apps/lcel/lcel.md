## Langchain Expression Language（LCEL）快速入门

LCEL 是 LangChain 中的一个重要概念，**LCEL是一种声明式的链式组合语言**。它提供了一种统一的接口，允许不同的组件（如 `retriever`, `prompt`, `llm` 等）可以通过统一的 `Runnable` 接口连接起来。每个 `Runnable` 组件都实现了相同的方法，如 `.invoke()`、`.stream()` 或 `.batch()`，这使得它们可以通过 `|` 操作符轻松连接。

### LCEL 的优势

LCEL使得从基本组件构建复杂链变得容易，并支持流式处理、并行处理和日志记录等开箱即用的功能。

* **统一接口**: LCEL 通过 `Runnable` 接口将不同的组件统一起来，简化了复杂操作的实现。
* **模块化**: 各个组件可以独立开发和测试，然后通过 LCEL 轻松集成。
* **可扩展性**: LCEL 支持异步调用、批处理和流式处理，适应不同的应用场景。

### 组件

我们已学习的组件包括以下模块：

#### 📃 Model I/O：

这包括提示管理，提示优化，用于聊天模型和LLM的通用接口，以及处理模型输出的常见实用工具。

#### 📚 Retrieval：

检索增强生成涉及从各种来源加载数据，准备数据，然后在生成步骤中检索数据以供使用。

#### 🤖 Agents：

Agents 允许LLM自主完成任务。 Agents会决定采取哪些行动，然后执行该行动，并观察结果，并重复此过程直到任务完成。 LangChain为代理提供了标准接口、可选择的代理列表以及端到端代理示例。

### 使用 LCEL 实现 LLMChain（Prompt + LLM)

#### Pipe 管道操作符

我们使用LCEL的 `|` 操作符将这些不同组件拼接成一个单一链。

**在这个链中，用户输入被传递到提示模板，然后提示模板的输出被传递到模型，接着模型的输出被传递到输出解析器。**

```
chain = prompt | model | output_parser
```

竖线符号类似于Unix管道操作符，它将不同的组件链接在一起，将一个组件的输出作为下一个组件的输入。



## 核心概念：invoke 方法

Langchain `invoke` 方法是 LCEL 设计中的重要方法，可以帮助开发者更高效地处理复杂任务，结合语言模型进行系统构建，实现不同数据源和API的接口对接。

### 基础概念

* 在Langchain中，invoke方法是所有LangChain表达式语言（LCEL）对象的通用同步调用方法。通过invoke方法，开发者可以直接调用LLM或ChatModel，简化了调用流程，提高了开发效率。
* 与其他链式调用方法相比，invoke方法更加灵活便捷，可以直接对输入进行调用，而不需要额外的链式操作。相对于batch和stream等异步方法，invoke方法更适用于单一操作的执行。

### 使用方式

* 单次调用：通过invoke方法，开发者可以快速对单一操作进行执行，例如转换ChatMessage为Python字符串等简单操作，提升了代码的可读性和整洁度。
* 复杂协作：Langchain的核心理念就是将语言模型作为协作工具，invoke方法可以很好地实现开发者与语言模型的高效互动，构建出处理复杂任务的系统，并对接不同的数据源和API接口。


## invoke 与 Model I/O 的结合

整个流程按照以下步骤进行：

1. `Prompt` 组件接收用户输入 **{"topic": "程序员"}**，然后使用该 topic 构建 `PromptValue`
2. `Model` 组件获取生成的提示，并传递给 GPT-3.5-Turbo 模型进行评估。从模型生成的输出是一个ChatMessage对象。
3. 最后，`output_parser` 组件接收ChatMessage，并将其转换为Python字符串，在invoke方法中返回。

### Prompt

`prompt` 是 `BasePromptTemplate` 的实例，这意味着它接受模板变量的字典并生成一个`PromptValue`。

PromptValue是一个包装器(wrapper)，围绕完成的提示进行操作，可以传递给LLM（以字符串作为输入）或ChatModel（以消息序列作为输入）。

它可以与任何语言模型类型一起使用，因为它定义了生成`BaseMessages`和生成字符串的逻辑。
