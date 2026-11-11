from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

@tool(description="查询体重")
def get_weight()->int:
    return 90

@tool(description="查询身高")
def get_height()->int:
    return 172

agent = create_agent(
    model = ChatOllama(model = "qwen3:1.7b"),
    tools = [get_height,get_weight],
    system_prompt = '''你是严格遵循ReAct框架的智能体，必须按[思考->行动->观察->再思考]的流程解决问题，
    且**每轮仅能思考并调用1个工具**，禁止单次调用多个工具。
    并告知我你的思考过程，工具调用的原因，按思考、行动、观察三个结构告知我'''
)

responses = agent.stream( {"messages": [ {"role":"user","content":"请计算BMI"} ]},
              stream_mode = "values"
             )
for res in responses:
    latest_message = res["messages"][-1]
    if latest_message.content:
        print(type(latest_message).__name__,latest_message.content)

    try:
        if latest_message.tool_calls:
            tool_list = [ tc["name"] for tc in latest_message.tool_calls ]
            print(tool_list)
    except AttributeError:
        pass




