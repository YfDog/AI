import os, json
from typing import Sequence

from langchain_community.chat_models import ChatTongyi
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import  ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory

'''
messages_from_dict:
[{},{},{}...] -> [消息，消息，消息...]  
【消息指的是BaseMessage类实例，像AIMessage、HumanMessage、SystemMessage都是BaseMessage类的子类】
因此AIMessage、HumanMessage、SystemMessage也属于消息的一种，可以将字典转换为AIMessage、HumanMessage、SystemMessage
'''


# FileChatMessageHistory类
class FileChatMessageHistory(BaseChatMessageHistory):  # BaseChatMessageHistory类是FileChatMessageHistory类的子类
    def __init__(self, session_id, storage_path):
        self.session_id = session_id  # 会话ID，会话ID区分不同的用户会话历史消息记录，在这里session_id就是最终的文件名
        self.storage_path = storage_path  # 会话ID对应的用户历史消息记录的文件夹存储路径
        # 完整文件路径
        self.file_path = os.path.join(self.storage_path, self.session_id)
        # 上面一行代码：示例：self.storage_path = "./chat_history"，self.session_id = "admin_user"
        # 最终拼接为（WIN系统下）：.\chat_history\admin_user
        # 也就是文件路径self.file_path=.\chat_history\admin_user

        # 根据file_path的路径先建立文件夹，文件夹若是已经存在则跳过不报错
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(
            self.messages)  # 这个messages是父类BaseChatMessageHistory的成员变量messages，该messages的类型是list[BaseMessage]
        # 为了确保兼容性，list类型的messages再强制类型转换成list类型
        # all_messages = list(self.messages)表示已有的消息列表
        all_messages.extend(messages)

        # 上面两行是在内存中进行操作的，下面要把内存中的数据写入本地文件。
        # 但是BaseMessage类消息对象直接写入文件是一串二进制，要先进行处理
        # 将BaseMessage类消息对象转为字典（借助json模块以json形式写入文件）
        '''
        这样其实就能实现，不过有更简单的写法，效果是一样的
        new_messages = []
        for message in all_messages:
            dict_message = message_to_dict(message)
            new_messages.append(dict_message)
        '''
        # 更简单的写法
        new_messages = [message_to_dict(message) for message in all_messages]

        # 做好处理后，将数据写入文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f, ensure_ascii=False, indent=2)

    # 打开文件，读出文件里的全部内容，将其转为列表【消息】返回
    @property  # @property装饰器将message方法变成类成员属性来使用
    def messages(self) -> list[BaseMessage]:
        # 经过add_messages方法后，使用本方法前，当前文件内的内容形式为：list[字典，字典，...]
        # 要将list[字典(json格式)，字典，...] 转为 list[消息，消息，...]
        # 文件现在在本地里，对文件进行操作，文件操作很容易发生异常，要考虑到异常情况
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)



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
#store = {}  # 通过字典去维护不同session_id的对话历史消息，也就是InMemoryChatMessageHistory类对象
            # key：session_id，value：对话历史消息，也就是InMemoryChatMessageHistory类对象
# def get_history(session_id): #从会话历史信息的临时存储变为长期存储主要要改这块的代码
#     if session_id not in store:
#         store[session_id] = InMemoryChatMessageHistory()
#     return store[session_id]  # 返回的是InMemoryChatMessageHistory类对象，也就是在内存里临时存放的对话历史消息

#从会话历史信息的临时存储变为长期存储主要要改这块的代码
#上面是在内存里临时储存，用字典，字典的键是session_id,字典的值是具体对话内容（是InMemoryChatMessageHistory类对象，也就是在内存里临时存放的对话历史消息）
# 下面是用文件储存，一个文件对应一个session_id，文件本身储存的就是会话历史消息
def get_history(session_id):
    return  FileChatMessageHistory(session_id,"./chat_history")


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

#先注释掉第3次运行的代码，运行。运行结束后，当前目录会出现有会话历史文件
#再将前两次运行的代码注释，第3次运行的代码不注释，运行。仍能正常回答问题，因为会读取文件的历史消息内容。
