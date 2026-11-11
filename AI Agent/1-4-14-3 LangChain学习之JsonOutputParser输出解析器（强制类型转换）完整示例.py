from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser,JsonOutputParser

model = ChatTongyi(model="qwen3.7-max")

#first_prompt_template = PromptTemplate.from_template("我的邻居姓：{lastname}，生了{gender}，请帮忙取个名字。要返回json格式。")
first_prompt_template = PromptTemplate.from_template("我的邻居姓：{lastname}，生了{gender}，请帮忙取个名字，"
                                                     "并封装为json格式返回给我，要求key是name，value是你起的名字。请严格遵守格式要求。")
#原提示词：我的邻居姓：{lastname}，生了{gender}，请帮忙取个名字，仅回复我姓名，无需额外内容。
#上述提示词给到模型，模型的输出结果就只有姓名（也就是一个字符串），无法转成json格式类型。
#要对提示词进行修改。

second_prompt_template = PromptTemplate.from_template("姓名：{name}，请帮我解析含义。")

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

chain = first_prompt_template|model|json_parser | second_prompt_template |model|str_parser
# model输出的是AIMessage类型，里面存放的就只有一个字符串："孙婉清"。
# 转成json格式，json解析器一脸懵逼，json格式要有键和值两个，如{"name":"孙婉清"}
# 可是model给到的输出只有一个字符串"孙婉清"，json解析器就懵逼了——这个字符串"孙婉清"是应该给键还是给值？
# 为了解决这个问题，model输出时就应该是json格式
# 也就是要改进first_prompt_template的提示词

responses = chain.invoke({"lastname":"孙","gender":"女儿"}) #为了良好的用户体验，invoke可以改为stream流式输出
print(responses)
print(type(responses))

