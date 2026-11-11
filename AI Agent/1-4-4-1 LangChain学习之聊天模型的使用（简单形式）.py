from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage

model = ChatTongyi(model="qwen3-max")

messages = [ #聊天模型消息的简写。简写情况下，就不需要导包和类了。
    #(角色，内容),角色仅system、human、ai
    ("system","你是一个边塞诗人。"),
    ("human","写一首唐诗。"),
    ("ai","锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。"),
    ("human","按照你上一个回复的格式，再写一首唐诗。")
]

responses = model.stream(input=messages)

for chunk in responses:
    print(chunk.content,end='',flush=True)