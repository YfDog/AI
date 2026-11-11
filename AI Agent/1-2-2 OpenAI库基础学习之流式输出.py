from openai import OpenAI

#1.创建客户端对象
client = OpenAI(
    # api_key 已经保存在环境变量里，这里可以不写。
    base_url = 'https://ws-whoz5a0rq16iacy9.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
)

#2.访问模型
response = client.chat.completions.create(
    model = "qwen3-max",
    messages = [
        {"role":"system","content":"你是Python代码专家，擅长将用户的问题用代码去解决，你话很多"},
        {"role":"assistant","content":"好的，我是一个Python代码专家,话很多"},
        {"role":"user","content":"1到10求和是多少？"}
    ],
    stream = True #流式输出设置
)

#3.处理结果
for chunk in response: #流式输出要搭配for循环使用
    print(chunk.choices[0].delta.content,
          end='',
          flush=True
        )

