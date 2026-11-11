from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate

from langchain_core.output_parsers import StrOutputParser

model = ChatTongyi(model="qwen3.7-max")

first_prompt_template = PromptTemplate.from_template("我的邻居姓：{lastname}，刚生了{gender}，请帮忙取个名字。就一个姓名。仅告知我姓名，不要额外信息。")
#原提示词：我的邻居姓：{lastname}，刚生了{gender}，请帮忙取个名字。
#上面的提示词模型会输出一堆内容，运行也能正常运行，只是比较消耗token。

second_prompt_template = PromptTemplate.from_template("姓名是：{name}，请解析一下含义")

str_parser = StrOutputParser()


chain = first_prompt_template | model | (lambda ai_msg:{"name":ai_msg.content}) | second_prompt_template | model | str_parser
#|在执行时会将函数自动转换为RunnableLambda类型，满足入链条件
'''
一次性输出：
responses = chain.invoke({"lastname":"孙","gender":"女儿"})
print(responses)
'''

for res in chain.stream({"lastname":"孙","gender":"女儿"}): #流式输出
    print(res,end="",flush=True)