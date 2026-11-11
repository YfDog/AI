from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage  #这3个消息类别类按实际需求导入
#需要设定一下系统角色就导入SystemMessage类
#需要类似于历史消息的模型回答就导入AIMessage类(要搭配HumanMessage使用)
#一般情况下，HumanMessage是在使用聊天模型至少要有的

chat_model = ChatTongyi(model = "qwen3-max")

messages = [
    SystemMessage(content="你是一个边塞诗人。"),
    HumanMessage(content="给我写一首唐诗"),
    AIMessage(content="锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。"),
    HumanMessage(content="按照你上一个回复的格式，再写一首唐诗。")
]

responses = chat_model.stream(input=messages)

for chunk in responses:
    print(chunk.content,end="",flush=True)  #聊天模型的chunk不能直接输出，要.content，取出chunk里的content内容


'''
使用Ollama本地模型的代码：
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage

model = ChatOllama(model='qwen3:4b')

messages = [
    SystemMessage(content="你是一个边塞诗人。"),
    HumanMessage(content="给我写一首唐诗"),
    AIMessage(content="锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。"),
    HumanMessage(content="按照你上一个回复的格式，再写一首唐诗。")
]

result = model.stream(input=messages)

for chunk in result:
    print(chunk.content,end='',flush=True)
'''