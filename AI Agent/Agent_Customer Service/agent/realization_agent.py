from langchain.agents import create_agent
from model.factory import chat_model
from utils.prompts_loader import load_system_main_prompt
from agent.tools.agent_tools import get_weather,get_user_id,get_current_month,get_user_city,rag,fetch_external_data,fill_context_for_report
from agent.tools.middleware import monitoring_tool_execute,log_before_model,prompt_switch


class RealizationAgent(object):
    def __init__(self):
        self.agent = create_agent(
            model = chat_model,
            system_prompt = load_system_main_prompt(),
            tools=[get_weather, get_user_id, get_current_month, get_user_city, rag, fetch_external_data, fill_context_for_report],
            middleware = [monitoring_tool_execute, log_before_model, prompt_switch],
        )

    def execute_agent(self,query:str):
        input_dict = {
            "messages":[
                {"role":"user", "content":query},
            ]
        }
        # 第三个参数context就是上下文runtime中的信息，就是做提示词切换的标记
        responses = self.agent.stream(input_dict, stream_mode="values", context={"report": False})
        for chunk in responses:
            latest_message = chunk["messages"][-1]

            if latest_message.content:
                yield latest_message.content.strip()+"\n"

# if __name__ == '__main__':
#     responses = RealizationAgent().execute_agent("在我当前的城市的天气下扫地机器人如何保养")
#     for res in responses:
#         print(res, end="", flush=True)





