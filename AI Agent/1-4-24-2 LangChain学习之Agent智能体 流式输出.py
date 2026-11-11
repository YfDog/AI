from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_ollama import ChatOllama


@tool(description="传入股票名称，获取该股票的股价，返回字符串信息")  #description参数能让模型知道这个工具是干什么的，方便模型更好的调用工具完成任务
def get_price(name:str)->str:
    return f"股票{name}的股价是23元"

@tool(description="传入股票名称，可以获得该股票的基本信息，返回字符串信息")
def get_infor(name:str)->str:
    return f"股票{name}是一家A股上市公司，专注于IT职业教育。"

agent = create_agent(
    model = ChatOllama(model="qwen3:1.7b"),
    tools = [get_price,get_infor],
    system_prompt = "你是一个智能助手，可以回答股票相关的问题，记住请告知我思考过程，让我知道你为什么调用某个工具。"
)

responses = agent.stream(
    {"messages":[{"role":"user","content":"传智教育的股价是多少，顺便也简单介绍一下"}]},
    stream_mode="values"  #values 获取完整流式输出结果
    )

for res in responses:
    latest_message = res["messages"][-1]
    if latest_message.content:
        print(type(latest_message).__name__,latest_message.content)
    try:
        if latest_message.tool_calls: #不是每一个消息都有tool_calls,因此要捕获一下异常
            tool_list = [tc["name"] for tc in latest_message.tool_calls]
            print(f"调用工具{tool_list}")
    except AttributeError:
        pass

# print("以下是模型执行流式的完整过程：")
# for res in responses:   #responses里是模型流式的返回结果，被res一点点拿走后，responses里就空了没有内容了
#     print(res)

# print("以下是取出messages键所对应的值：")
# for res in responses:
#     print(res["messages"])

# print("以下是只要列表的最后一个元素，也就是最新更新的元素：")
# for res in responses:
#     print(res["messages"][-1])  #只要列表的最后一个元素，也就是最新更新的元素

# print("以下是只要列表的最后一个元素的content属性：")
# for res in responses:
#     print(res["messages"][-1].content)  #只要列表的最后一个元素的content属性

# print("以下是只要列表的最后一个元素的content属性并且这条消息是什么类型：")
# for res in responses:
#     print(type(res["messages"][-1]).__name__,res["messages"][-1].content)



