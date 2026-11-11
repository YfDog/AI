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
        {"role":"system","content":"你是Python代码专家，擅长将用户的问题用代码去解决，你不说废话且回答简洁"},
        {"role":"assistant","content":"好的，我是一个Python代码专家,话不多且回答简洁"},
        {"role":"user","content":"1到10求和是多少？"}
    ]
)

#3.处理结果
print(response.choices[0].message.content)

