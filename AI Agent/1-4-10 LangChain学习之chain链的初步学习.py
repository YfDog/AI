from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system","你是一个田园诗人。极其擅长将田园风光和见闻写成优美的诗篇。"),
        MessagesPlaceholder("history"),
        ("human","请你再写一首田园诗。")
    ]
)
history_data = [
    ("human","写一首田园诗"),
    ("ai","明月别枝惊鹊，清风半夜鸣蝉。稻花香里说丰年，听取蛙声一片。七八个星天外，两三点雨山前。旧时茅店社林边，路转溪桥忽见。"),
    ("human","再写一首田园诗"),
    ("ai","绿波春浪满前陂，极目连云罢亚肥。更被鹭鹚千点雪，破烟来入画屏飞。"),
    ("human","写的好，再来一首"),
    ("ai","石梁茅屋有弯碕，流水溅溅度两陂。晴日暖风生麦气，绿阴幽草胜花时。"),
]
#prompt_chat = chat_prompt_template.invoke({"history":history_data})

model = ChatTongyi(model="qwen3-max")

#result = model.invoke(input=prompt_chat)
#print(result.content)

chain = chat_prompt_template | model #链的运行是从左到右的

#invoke的{"history":history_data}作为chain链的原始输入,输入给chat_prompt_template，chat_prompt_template的输出是model的输入
responses = chain.invoke({"history":history_data}) #用stream也可以
print(responses.content)





