from openai import OpenAI
import json

client = OpenAI(
    #api_key 已保存在环境变量里，这里可以不写
    base_url = "https://ws-whoz5a0rq16iacy9.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    #base_url = "http://localhost:11434/v1"   这个是调用本地模型Ollama的URL地址
)

attribute_schema = ["日期","股票名称","开票价","收盘价","成交量"] #要提取出文本的这六个属性信息
examples_data = [ #few-shot少样本方法，给模型的参考示例数据
    {
       "content":"2023-01-10,股市震荡。股票强大科技A股今日开盘价100人民币，一度飙升至105人民币，随后回落至98人民币，最终以102人民币收盘，成交量达到52000",
        "answers":{
            "日期":"2023-01-10",
            "股票名称":"强大科技A股",
            "开盘价":"100人民币",
            "收盘价":"102人民币",
            "成交量":"520000"
        }
    },
    {
        "content":"2024-05-16，股市利好。股票英伟达美股今日开票价105美元，一度飙升至109美元，随后回落至100美元，最终以116美元收盘，成交量达到3560000",
        "answers":{
            "日期":"2024-05-16",
            "股票名称":"英伟达美股",
            "开盘价":"105美元",
            "收盘价":"116美元",
            "成交量":"3560000"
        }
    }
]
questions = [
    "2025-06-16,股市利好。股票传智教育A股今日开盘价66人民币，一度飙升至70人民币，随后回落至65人民币，最终以68人民币收盘，成交量达到123000",
    "2025-06-06,股市利好。股票黑马程序员A股今日开盘价200人民币，一度飙升至211人民币，随后回落至201人民币，最终以206人民币收盘"
]

'''
代码中的messages部分：

[   #系统角色设定部分
    {"role":"system","content":f"你帮我完成信息抽取，我给你句子，你抽取{attribute_schema}信息，按json字符串输出，如果某些信息不存在，用'原文未提及'表示，请参考如下示例："},
    
    #历史消息记录，也是few-shot少样本方法提示词撰写，给模型参考示例的部分
    {"role":"user","content":"2023-01-10,股市震荡。股票强大科技A股今日开盘价100人民币，一度飙升至105人民币，随后回落至98人民币，最终以102人民币收盘，成交量达到52000"},
    {"role":"assistant","content":"{"日期":"2023-01-10","股票名称":"强大科技A股","开盘价":"100人民币","收盘价":"102人民币","成交量":"520000"}" },
    
    {"role":"user","content":"2024-05-16，股市利好。股票英伟达美股今日开票价105美元，一度飙升至109美元，随后回落至100美元，最终以116美元收盘，成交量达到3560000"},
    {"role":"assistant","content":"{"日期":"2024-05-16","股票名称":"英伟达美股","开盘价":"105美元","收盘价":"116美元","成交量":"3560000"}"},
    
    #用户的最新问题
    {"role":"user","content":f"按照上述示例，现在抽取这个句子的信息：{具体要抽取的文本，到时候替换}"},
]
'''

messages = [
    {"role":"system","content":f"你帮我完成信息抽取，我给你句子，你抽取{attribute_schema}信息，按json字符串输出，如果某些信息不存在，用'原文未提及'表示，请参考如下示例："}
]
for examples in examples_data:
    messages.append({"role":"user","content":examples["content"]})
    messages.append({"role": "assistant", "content":json.dumps(examples["answers"],ensure_ascii = False)}) #ensure_ascii = False 可以规避中文乱码问题
for mes in messages:
    print(mes)


print("下面是模型回复用户问题：")
for que in questions:
    responses = client.chat.completions.create(
        model = "qwen3-max",  #若是用本地模型Ollama，这里就替换为本地下载的模型名称，如：qwen3:4b
        messages = messages+[{"role":"user","content":f"按照上述示例，现在抽取这个句子的信息：{que}"}],
    )
    print(responses.choices[0].message.content)

