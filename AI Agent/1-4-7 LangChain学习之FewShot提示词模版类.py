from langchain_core.prompts import FewShotPromptTemplate,PromptTemplate
from langchain_community.llms.tongyi import Tongyi

model = Tongyi(model="qwen-max")

prompt_template = PromptTemplate.from_template("词:{word}，反义词:{antonym}") #占位符必须包含在双引号里，也就是占位符本身是字符串

examples_data = [ #示例数据是列表嵌套字典
    {"word":"大","antonym":"小"},
    {"word":"上","antonym":"下"},
]

few_shot_prompt = FewShotPromptTemplate(
    example_prompt = prompt_template,
    examples = examples_data,
    prefix = "我会给你一个词，请你给我该词的反义词，有如下示例：",
    suffix = "请参照上述示例，给出{input_word}的反义词",
    input_variables = ["input_word"]  #列表形式，如果有需要可以在列表里写多个需要注入的变量
)#这里的提示词组织不完全等同于历史消息，这只有一次用户信息，历史消息是多轮对话，会有多个用户信息和AI回答信息

prompt_text = few_shot_prompt.invoke(input={"input_word":"左"}).to_string() #few_shot_prompt实例对象使用invoke方法对占位符的变量进行信息的注入
print(prompt_text)

print("\n"+"以下为模型回复内容：")

responses = model.invoke(input=prompt_text)
print(responses)
