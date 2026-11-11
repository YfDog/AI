'''
本文件实现的是中间件：
1.monitoring_tool_execute  [监控工具的调用执行][工具调用时]
2.log_before_model         [模型执行前的监控工具]
3.prompt_switch            [提示词切换工具]（平时用main_prompt提示词，当用户有报告生成的需求时切换为report_prompt提示词）
'''
from typing import Callable
from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain_core.messages import ToolMessage
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.runtime import Runtime
from langgraph.types import Command
from utils.logger_handler import logger
from utils.prompts_loader import load_report_prompt,load_system_main_prompt


@wrap_tool_call
def monitoring_tool_execute(
        #request是传给模型的请求参数（像提示词、模型名、温度等），这里面也装了这次要调用哪个工具、传了什么参数
        #request：请求数据的封装
        request:ToolCallRequest,

        #handler是原本真正调用大模型的原生函数，也是真正要跑的工具业务函数！监控函数只是把它包起来
        #handler：执行函数本身
        handler:Callable[[ToolCallRequest],ToolMessage|Command]
) -> ToolMessage | Command:
    logger.info(f"[tool monitor]执行工具：{request.tool_call['name']}")
    logger.info(f"[tool monitor]传入参数：{request.tool_call['args']}")

    try:
        result = handler(request)
        logger.info(f"[tool monitor]工具{request.tool_call['name']}调用成功")

        if request.tool_call['name'] == "fill_context_for_report":
            request.runtime.context["report"] = True

        return result
    except Exception as e:
        logger.error(f"[tool monitor]工具{request.tool_call['name']}调用失败，原因：{e}")
        raise e


@before_model
def log_before_model(state:AgentState,runtime:Runtime):
    '''
    :param state: 整个Agent智能体的状态记录
    :param runtime: 记录了整个执行过程的上下文信息
    :return:
    '''
    logger.info(f"[log_before_model]现在模型还未调用，模型即将调用，带有{len(state['messages'])}条消息")
    logger.debug(f"[log_before_model]{type(state['messages'][-1]).__name__}:{state['messages'][-1].content}")

    return None

@dynamic_prompt  #每一次向模版注入信息之前调用此函数
def prompt_switch(request:ModelRequest):  #动态切换提示词
    is_report = request.runtime.context.get("report",False)  #键值report拿不到True默认为False
    if is_report:
        return load_report_prompt()

    return load_system_main_prompt()






