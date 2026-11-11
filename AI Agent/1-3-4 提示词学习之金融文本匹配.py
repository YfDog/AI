from openai import OpenAI

client = OpenAI(
    #api_key 已保存在环境变量里，这里可以不写
    base_url = "https://ws-whoz5a0rq16iacy9.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    #base_url = "http://localhost:11434/v1"   这个是调用本地模型Ollama的URL地址
)
examples_data = {  #few-shot少样本方法，给模型的参考示例数据
    "是":[
        ("公司ABC发布了季度财报，显示盈利增长。","财报披露，公司ABC利润上升。"),
        ("公司ITCAST发布了年度财报，显示盈利大幅度增长。","财报披露，公司ITCAST更赚钱了。")
    ],
    "不是":[
        ("黄金价格下跌，投资者抛售。","外汇市场交易额创下新高。"),
        ("央行降息，刺激经济增长。","新能源技术的创新。")
    ]
}
questions = [
    ("利率上升，影响房地产市场。","高利率对房地产有一定的冲击。"),
    ("油价大幅度下跌，能源公司面临挑战。","未来智能城市的建设趋势越加明显。"),
    ("股票市场今日大涨，投资者乐观。","持续上涨的市场让投资者感到满意。")
]

"""
代码中的messages部分：

[   #系统角色设定部分
    {"role":"system","content",f"你帮我完成文本匹配，我给你两个句子，被[]包围，你判断它们是否匹配，回答是或不是，请参考如下示例:"},
    
    #历史消息记录，也是few-shot少样本方法提示词撰写，给模型参考示例的部分
    {"role":"user","content":"句子1：[公司ABC发布了季度财报，显示盈利增长。]句子2：[财报披露，公司ABC利润上升。]"},
    {"role":"assistant","content":"是"},
    
    {"role":"user","content":"句子1：[公司ITCAST发布了年度财报，显示盈利大幅度增长。]句子2：[财报披露，公司ITCAST更赚钱了。]"},
    {"role":"assistant","content":"是"},
    
    {"role":"user","content":"句子1：[黄金价格下跌，投资者抛售。]句子2：[外汇市场交易额创下新高。]"},
    {"role":"assistant","content":"不是"},
    
    {"role":"user","content":"句子1：[央行降息，刺激经济增长。]句子2：[新能源技术的创新。]"},
    {"role":"assistant","content":"不是"},
    
    #用户的最新提问
    {"role":"user","content":f"按照上述示例，请回答下面这两个句子是否匹配。句子1：[......]，句子2：[......]"},
]
"""

messages = [
    {"role":"system","content":f"你帮我完成文本匹配，我给你两个句子，被[]包围，你判断它们是否相关联，回答是或不是，请参考如下示例:"},
]
'''
for key,value in examples_data.items():
    messages.append({"role":"user","content":value})
    messages.append({"role": "assistant", "content": key})
for mes in messages:
    print(mes)
这种逻辑确实是能够把信息存入messages里，但不是我们想要的格式
'''
for key,value in examples_data.items():
    for val in value:
        messages.append({"role":"user","content":f"句子1：[{val[0]}],句子2：[{val[1]}]"})
        messages.append({"role": "assistant", "content": key})
for mes in messages:
    print(mes)

print("下面为大模型回复用户问题：")
for que in questions:
    responses = client.chat.completions.create(
        model = "qwen3-max",    #若是用本地模型Ollama，这里就替换为本地下载的模型名称，如：qwen3:4b
        messages = messages+[{"role":"user","content":f"按照上述示例，请回答下面这两个句子是否匹配。句子1：[{que[0]}]，句子2：[{que[1]}]"}],
    )
    print(responses.choices[0].message.content)

