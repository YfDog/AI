from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system","你是一个田园诗人，擅长将田园风光和见闻写成一首朗朗上口诗。"),
        MessagesPlaceholder("history"),
        ("human","现在请再写一首田园诗。")
    ]
)

history_data = [
    ("human","现在写一首田园诗"),
    ("ai","故人具鸡黍，邀我至田家。绿树村边合，青山郭外斜。开轩面场圃，把酒话桑麻。待到重阳日，还来就菊花。"),
    ("human","再来一首诗"),
    ("ai","雨里鸡鸣一两家，竹溪村路板桥斜。妇姑相唤浴蚕去，闲着中庭栀子花。")
]

prompt = chat_prompt_template.invoke({"history":history_data})
print("ChatPromptTemplate类的实例对象prompt（也就是chat_prompt_template）的返回值类型是ChatPromptValue：",type(prompt))
print()
print(prompt.to_string()) #prompt类型是ChatPromptValue，不是字符串，控制台输出打印的不是我们想要的内容，要转为字符串才行。
#print(prompt.messages.content) 这种写法是错误的

print("下面是模型的回复内容：")
model = ChatTongyi(model="qwen3-max")
response = model.invoke(input=prompt)
print(response.content)

print("response的类型是AIMessage：",type(response))
print("response.content的类型是str：",type(response.content))


