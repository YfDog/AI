from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.tools import tool

@tool(description="查询天气") #普通的函数是无法作为工具使用的，需要tool装饰器，description用于描述这个工具是用来干什么的
def get_weather()->str:
    return "晴朗"

#创建智能体
agent = create_agent(
    model = ChatOllama(model = "qwen3:1.7b"), #智能体的大脑是哪个模型
    tools = [get_weather], #有哪些工具可以供智能体调用
    system_prompt = "你是一个聊天助手，可以回答用户的问题"
)

responses:dict = agent.invoke({"messages":[{"role":"user","content":"明天广东的天气如何？"},] })

print("这是模型回复的原封不动的内容：\n",responses,"\n\n")
print("这是模型回复内容里取出messages键对应的值：\n",responses["messages"],"\n\n")

for res in responses["messages"]:
    print(type(res),res.content)

for res in responses["messages"]:
    print(type(res).__name__,res.content)

