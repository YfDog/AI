from langchain_community.llms.tongyi import Tongyi

model = Tongyi(model='qwen-max') #访问的是大语言模型，而不是聊天模型，阿里云大语言模型的名称是qwen-max

#想实现流式输出，就把先前学习的invoke方法替换为stream方法
result = model.stream(input="你是谁？你能做什么？") #invoke方法是一次性得到大模型回答的结果

for chunk in result:
    print(chunk,end='',flush=True) #大语言模型取到的chunk可以直接打印出来

'''
本地模型Ollama的代码（流式输出）：

from langchain_ollama import OllamaLLM

model = OllamaLLM(model='qwen3:4b')

result = model.stream(input='你是谁？你能做什么？')

for chunk in result:
    print(chunk,end='',flush=True)
'''