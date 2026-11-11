#from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt_template = PromptTemplate.from_template("你是一个{category}诗人，"
                             "很擅长将{category}风光和见闻写成诗篇。")

model = ChatTongyi(model="qwen3.7-max") #聊天模型qwen3-max已于2026年10月10号下线

str_parser = StrOutputParser()

chain = prompt_template | model | str_parser | model

responses = chain.invoke({"category":"田园"})

print(responses.content) #返回的消息类型是AIMessage，想取出里面的内容就要.content
print(type(responses))
# 如果想实现print(responses)，可以在chain链的末尾再加一个str_parser将AIMessage类型转换为str类型，就不用.content

