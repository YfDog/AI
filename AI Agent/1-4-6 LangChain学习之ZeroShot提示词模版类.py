# Zero-Shot 这种也是通用提示词模版

from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi

model = Tongyi(model="qwen-max")

'''
lastname = "张"
gender = "女儿"
s = f"我的邻居姓：{lastname}，生了个{gender}，请帮忙取一个好听的名字。"
以上也能实现形成完整字符串，但是跟提示词模版不同的是。提示词模版可以加入LangChain的执行链，
而直接写成字符串是加入不了执行链的。链是LangChain的核心用法。
'''
prompt_template = PromptTemplate.from_template(
    "邻居姓：{lastname}，生了个{gender}，请帮忙取一个好听的名字。"
)
prompt_str = prompt_template.format(lastname="张",gender="女儿") #prompt_template实例对象用format方法对占位符的变量进行信息的注入

responses = model.invoke(input=prompt_str)


print(responses)
