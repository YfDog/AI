from openai import OpenAI
import os

client = OpenAI(
    api_key= os.getenv("OPENAI_API_KEY"),
    base_url = "https://ws-whoz5a0rq16iacy9.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

messages = [{"role":"user","content":"你能干什么？"}]

completion = client.chat.completions.create(
    model = "qwen3-max",
    messages = messages,
    extra_body = {"enable_thinking":True},
    stream = True
)

is_answering = False
print("\n" + "="*20 + "思考过程" + "="*20)

for chunk in completion:
    if not chunk.choices:
        continue
    delta = chunk.choices[0].delta
    if hasattr(delta,"reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content,end='',flush=True)
    if hasattr(delta,"content") and delta.content:
        if not is_answering:
            print("\n" + "="*20 + "完整回复" + "="*20)
            is_answering = True
        print(delta.content,end='',flush=True)
