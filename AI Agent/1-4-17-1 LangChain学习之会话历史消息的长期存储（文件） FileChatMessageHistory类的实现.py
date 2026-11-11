import os,json
from typing import Sequence

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage

'''
messages_from_dict:
[{},{},{}...] -> [消息，消息，消息...]  
【消息指的是BaseMessage类实例，像AIMessage、HumanMessage、SystemMessage都是BaseMessage类的子类】
因此AIMessage、HumanMessage、SystemMessage也属于消息的一种，可以将字典转换为AIMessage、HumanMessage、SystemMessage
'''

#FileChatMessageHistory类
class FileChatMessageHistory(BaseChatMessageHistory): #BaseChatMessageHistory类是FileChatMessageHistory类的子类
    def __init__(self,session_id,storage_path):
        self.session_id = session_id       #会话ID，会话ID区分不同的用户会话历史消息记录，在这里session_id就是最终的文件名
        self.storage_path = storage_path   #会话ID对应的用户历史消息记录的文件夹存储路径
        # 完整文件路径
        self.file_path = os.path.join(self.storage_path,self.session_id)
        #上面一行代码：示例：self.storage_path = "./chat_history"，self.session_id = "admin_user"
        #最终拼接为（WIN系统下）：.\chat_history\admin_user
        #也就是文件路径self.file_path=.\chat_history\admin_user

        #根据file_path的路径先建立文件夹，文件夹若是已经存在则跳过不报错
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)  #这个messages是父类BaseChatMessageHistory的成员变量messages，该messages的类型是list[BaseMessage]
                                            #为了确保兼容性，list类型的messages再强制类型转换成list类型
                                            #all_messages = list(self.messages)表示已有的消息列表
        all_messages.extend(messages)

        #上面两行是在内存中进行操作的，下面要把内存中的数据写入本地文件。
        #但是BaseMessage类消息对象直接写入文件是一串二进制，要先进行处理
        #将BaseMessage类消息对象转为字典（借助json模块以json形式写入文件）
        '''
        这样其实就能实现，不过有更简单的写法，效果是一样的
        new_messages = []
        for message in all_messages:
            dict_message = message_to_dict(message)
            new_messages.append(dict_message)
        '''
        #更简单的写法
        new_messages = [message_to_dict(message) for message in all_messages]

        #做好处理后，将数据写入文件
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump(new_messages,f,ensure_ascii=False,indent=2)

    #打开文件，读出文件里的全部内容，将其转为列表【消息】返回
    @property   #@property装饰器将message方法变成类成员属性来使用
    def messages(self) -> list[BaseMessage]:
        #经过add_messages方法后，使用本方法前，当前文件内的内容形式为：list[字典，字典，...]
        #要将list[字典(json格式)，字典，...] 转为 list[消息，消息，...]
        #文件现在在本地里，对文件进行操作，文件操作很容易发生异常，要考虑到异常情况
        try:
            with open(self.file_path,"r",encoding="utf-8") as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump([],f)
