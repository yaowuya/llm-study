# 文本内容补全初探（Completions API）

使用 Completions API 实现各类文本生成任务

主要请求参数说明：

- model （string，必填）
  要使用的模型的 ID。可以参考 模型端点兼容性表。
- prompt （string or array，必填，Defaults to ）
  生成补全的提示，编码为字符串、字符串数组、token数组或token数组数组。
  注意，这是模型在训练过程中看到的文档分隔符，所以如果没有指定提示符，模型将像从新文档的开头一样生成。
- stream （boolean，选填，默认 false）
  当它设置为 true 时，API 会以 SSE（ Server Side Event ）方式返回内容，即会不断地输出内容直到完成响应，流通过 data: [DONE] 消息终止。
- max_tokens （integer，选填，默认是 16）
  补全时要生成的最大 token 数。
  提示 max_tokens 的 token 计数不能超过模型的上下文长度。大多数模型的上下文长度为 2048 个token（最新模型除外，它支持 4096）
- temperature （number，选填，默认是1）
  使用哪个采样温度，在 0和2之间。
  较高的值，如0.8会使输出更随机，而较低的值，如0.2会使其更加集中和确定性。
  通常建议修改这个（temperature ）或 top_p 但两者不能同时存在，二选一。
- n （integer，选填，默认为 1）
  每个 prompt 生成的补全次数。
  注意：由于此参数会生成许多补全，因此它会快速消耗token配额。小心使用，并确保对 max_tokens 和 stop 进行合理的设置。


# 聊天机器人初探（Chat Completions API）

使用 Chat Completions API 实现对话任务

聊天补全(Chat Completions API)以消息列表作为输入，并返回模型生成的消息作为输出。尽管聊天格式旨在使多轮对话变得简单，但它同样适用于没有任何对话的单轮任务。

主要请求参数说明：

* **`model` （string，必填）**
  要使用的模型ID。有关哪些模型适用于Chat API的详细信息
* **`messages` （array，必填）**
  迄今为止描述对话的消息列表

  * **`role` （string，必填）**

  发送此消息的角色。`system` 、`user` 或 `assistant` 之一（一般用 user 发送用户问题，system 发送给模型提示信息）

  * **`content` （string，必填）**
    消息的内容
  * **`name` （string，选填）**
    此消息的发送者姓名。可以包含 a-z、A-Z、0-9 和下划线，最大长度为 64 个字符
* **`stream` （boolean，选填，是否按流的方式发送内容）**
  当它设置为 true 时，API 会以 SSE（ Server Side Event ）方式返回内容。SSE 本质上是一个长链接，会持续不断地输出内容直到完成响应。如果不是做实时聊天，默认false即可。
* **`max_tokens` （integer，选填）**
  在聊天补全中生成的最大 **tokens** 数。
  输入token和生成的token的总长度受模型上下文长度的限制。
* **`temperature` （number，选填，默认是 1）**
  采样温度，在 0和 2 之间。
  较高的值，如0.8会使输出更随机，而较低的值，如0.2会使其更加集中和确定性。
  通常建议修改这个（`temperature` ）或者 `top_p` ，但两者不能同时存在，二选一。
