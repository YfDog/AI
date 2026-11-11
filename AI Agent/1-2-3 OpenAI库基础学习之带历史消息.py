from openai import OpenAI

client:OpenAI = OpenAI(
    # api_key 已保存在环境变量里，这里可以不写
    base_url = 'https://ws-whoz5a0rq16iacy9.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
)

response = client.chat.completions.create(
    model = 'qwen3-max',
    messages = [
        {'role':'system','content':'你是AI助理，回答很简洁'},
        {'role':'user','content':'小明有两条宠物狗'},
        {'role':'assistant','content':'好的'},
        {'role':'user','content':'小红有三只宠物猫'},
        {'role':'assistant','content':'好的'},  #以上都是历史消息，记录在messages变量里
        {'role':'user','content':'总共有几个宠物'}
    ],
    stream = True
)

for chunk in response:
    print(chunk.choices[0].delta.content,end='',flush=True)


