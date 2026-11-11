'''
将用户与模型的对话过程打印出来发现，对话历史的消息格式不太符合人类习惯，控制台直接就将整个被封装的消息打印出来了
所以要将代码进行优化：
原先使用的通用提示词模版不够标准，对此进行改进，替换为Chat提示词模版
'''
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory  # 帮助创建新链，这个新链就有历史消息附加功能
from langchain_core.chat_history import InMemoryChatMessageHistory       # 内存临时存储

model = ChatTongyi(model="qwen3.7-max")
# prompt_template = PromptTemplate.from_template(
#    "你需要根据会话历史回应用户问题。对话历史：{chat_history}，用户输入：{user_input}。"
# )
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system","你需要根据会话历史回应用户问题。对话历史："),
        MessagesPlaceholder("chat_history"),
        ("human","用户输入：{user_input}")
    ]
)

str_parser = StrOutputParser()

#print打印对话过程
def print_prompt(complete_prompt):  #print打印对话过程
    print("="*20,complete_prompt.to_string(),"="*20)  #print("="*20,complete_prompt,"="*20)
    return complete_prompt
base_chain = prompt_template |print_prompt| model | str_parser

# 函数。实现通过会话ID获取InMemoryChatMessageHistory类对象，也就是临时储存在内存里的对话历史消息
store = {}  # 通过字典去维护不同session_id的对话历史消息，也就是InMemoryChatMessageHistory类对象
            # key：session_id，value：对话历史消息，也就是InMemoryChatMessageHistory类对象
def get_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]  # 返回的是InMemoryChatMessageHistory类对象，也就是在内存里临时存放的对话历史消息


# 创建一个新的链，该链对原有链的功能进行增强：新链可以自动附加历史消息
conversation_chain = RunnableWithMessageHistory(
    base_chain,  # 被增强的原有链。
    get_history,  # 自定义的函数，用于通过会话ID获取InMemoryChatMessageHistory类对象，
    # 也就是通过会话ID获取在内存临时存放的历史消息。
    input_messages_key="user_input",  # 在提示词模版中，用户输入用的是哪个占位符。
    history_messages_key="chat_history"  # 在提示词模版中，对话历史用的是哪个占位符。
)

if __name__ == '__main__':
    # 固定格式，为RunnableWithMessageHistory类对象能传入会话ID进行配置
    session_id_config = {
        "configurable": {"session_id": "admin_user"}
    }

    responses = conversation_chain.invoke({"user_input": "小明有2只猫"}, session_id_config)
    print("第1次运行：", responses)

    responses = conversation_chain.invoke({"user_input": "小红有3只狗"}, session_id_config)
    print("第2次运行：", responses)

    responses = conversation_chain.invoke({"user_input": "一共有几只宠物？"}, session_id_config)
    print("第3次运行：", responses)
"""
第1次运行，用户提问小明有2只猫，此时因为是用户第1次提问，对话历史还不存在，chat_history为空，第1次执行结束后，RunnableWithMessageHistory类对象会自动添加第1轮次对话历史进chat_history。
对话历史chat_history：Human：小明有2只猫，AIMessage：xxxxxx

第2次运行，用户提问小红有3只狗，此时是用户第2次提问，对话历史存在，chat_history不为空，第2次执行结束后，RunnableWithMessageHistory类对象会自动添加第2轮次对话历史进chat_history。
对话历史chat_history：Human：小明有2只猫，AIMessage：xxxxxx
                     Human：小红有3只狗，AIMessage：xxxxxx

第3次运行，用户提问一共有几只宠物？，此时是用户第3次提问，对话历史存在，chat_history不为空，第3次执行结束后，RunnableWithMessageHistory类对象会自动添加第3轮次对话历史进chat_history。
对话历史chat_history：Human：小明有2只猫，AIMessage：xxxxxx
                     Human：小红有3只狗，AIMessage：xxxxxx
                     Human：一共有几只宠物？，AIMessage：一共5只宠物
该对话历史消息归属为session_id是admin_user的用户。             
"""


