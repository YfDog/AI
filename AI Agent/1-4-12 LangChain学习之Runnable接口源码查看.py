from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi

prompt_template = PromptTemplate.from_template("你是一个AI助手")
model = ChatTongyi(model="qwen3-max")

chain = prompt_template | model

chain.invoke()
#或者 chain.stream()


#以上是LangChain中链的执行的简单框架
#以上组成链的逻辑是：需要先有提示词，然后有模型，再将提示词给到模型，
#chain链调用invoke()方法或stream()方法触发执行链，invoke()方法或stream()方法的数据作为原始输入
#给到执行链的prompt_template（提示词模版），形成完整的提示词输出，完整的提示词作为model的输入给到模型，然后模型给出回复。

