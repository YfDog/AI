'''
这块是整个RAG项目的核心
把整个链条串起来
'''
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, \
    RunnableLambda  # RunnablePassthrough 作用之一：原样透传输入，输入是什么，输出就返回什么，不改变
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from search_service import SearchServiceRetriever
from history_store import get_history
import config

def format_dispose(docs:list[Document]):
    if not docs:
        return "没有找到相关参考资料"

    reference_str = ""
    for doc in docs:
        reference_str += f"文档内容：{doc.page_content}\n元数据：{doc.metadata}\n\n"  #除了内容，还给了元数据，用于给模型更多的参考信息

    return reference_str

def print_prompt(completion_prompt):
    print("="*20+"以下是完整提示词"+"="*20)
    print(completion_prompt.to_string())
    return completion_prompt

# def temp1(data:dict):
#     print("-------",data) #用于chain链中retriever之前，在数据进入retriever之前将它打印出来，看看类型和内容是否匹配
#     return data

def format_for_retriever(data:dict) -> str :
    return data["user_input"]

# def temp2(data):
#     print("-------",data) #用于chain链中self.prompt_template之前，在数据进入self.prompt_template之前将它打印出来，看看类型和内容是否匹配
#     return data

def format_for_prompt_template(data):
    input = {}
    input["user_input"] = data["user_input"]["user_input"]
    input["history"] = data["user_input"]["history"]
    input["reference_content"] = data["reference_content"]
    return input


class RagService(object):
    def __init__(self):

        self.chat_model = ChatOllama(model= config.chat_model)

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system","以我提供的参考资料为主，简洁专业的回答用户问题。参考资料：{reference_content}"),
                ("system", "你必须严格使用【参考资料】里面的原文区间进行回答，一字一段从参考资料摘抄，禁止自己改写、"),
                ("system","并且我提供用户的历史对话记录，历史对话记录如下："),
                MessagesPlaceholder("history"),
                ("user","请回答用户问题：{user_input}")
            ]
        )
        #search_retriever，课程中名称为：vector_service
        self.search_retriever = SearchServiceRetriever()  #此时的检索器还入不了链

        self.chain = self.get_chain()

    def get_chain(self):
        '''获得最终的chain链'''
        #检索器链条化
        retriever = self.search_retriever.get_retriever()  #此时的检索器可以入链

        chain =( {"user_input":RunnablePassthrough(),
                  "reference_content": RunnableLambda(format_for_retriever) | retriever | format_dispose
                  } | RunnableLambda(format_for_prompt_template) |self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
                 )

        conversation_chain= RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key = "user_input",
            history_messages_key = "history"
        )

        return conversation_chain  #原来是return chain

if __name__ == '__main__':
    session_id_config = {
        "configurable": {"session_id": "admin_user"}
    }

    responses = RagService().chain.invoke({"user_input":"张三的身高169cm，体重126斤，请给张三推荐衣服尺码。"},session_id_config)
    print("这是模型的回复:",responses)

