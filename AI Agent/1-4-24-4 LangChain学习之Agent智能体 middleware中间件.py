from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_agent, after_agent, before_model, after_model, wrap_model_call, \
    wrap_tool_call
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.runtime import Runtime


@tool(description="查询天气")
def get_weather(city:str)->str:
    return f"城市{city}的天气是晴天"

@before_agent
def log_before_agent(state:AgentState,runtime:Runtime):  #形参名是固定的state、runtime【类型注解Runtime导入的是langgraph里的】
    #agent执行前会调用这个函数并传入state和runtime两个参数
    print(f"[before agent]现在在agent调用前，agent启动啦，并附带{len(state['messages'])}条消息")

@after_agent
def log_after_agent(state:AgentState,runtime:Runtime):
    print(f"[after agent]现在在agent执行结束后，agent结束啦，并附带{len(state['messages'])}条消息")

@before_model
def log_before_model(state:AgentState,runtime:Runtime):
    print(f"[before model]现在在模型执行前，模型即将调用，并附带{len(state['messages'])}条消息")

@after_model
def log_after_model(state:AgentState,runtime:Runtime):
    print(f"[after model]模型调用结束啦，并附带{len(state['messages'])}条消息")

@wrap_model_call #模型调用中的监控中间件
def model_call_hook(request,handler):
    print("模型调用啦")
    return handler(request)

@wrap_tool_call  #工具调用中的中间件
def tool_call_hook(request,handler):
    print(f"执行工具：{request.tool_call['name']}")
    print(f"工具执行传入参数：{request.tool_call['args']}")
    return handler(request)

agent = create_agent(
    model = ChatOllama(model="qwen3:1.7b"),
    tools = [get_weather],
    middleware = [tool_call_hook,model_call_hook,log_after_model,log_before_model,log_after_agent,log_before_agent],
    system_prompt="你是一个天气预报助手，给你城市名字，你能预报这个城市的天气。"
)
responses = agent.invoke({
    "messages":[
        {"role":"user","content":"深圳明天的天气怎么样？"}
    ]
})

print(responses)





