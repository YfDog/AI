from langchain_community.llms.tongyi import Tongyi  #使用阿里云云端模型，要导入的包和类的名称
#langchain_community已经不维护了，代码能正常运行，但是会报警告。
#学习阶段先用着

model = Tongyi(model="qwen-max")  #用类创建一个实例化对象。这句意思是要访问模型。

result = model.invoke(input="你是谁？你能做什么？")  #调用模型并对模型发起提问，获得模型的回复。

print(result)  #


'''
下面是用Ollama本地模型的代码：
from langchain_ollama import OllamaLLM

model = OllamaLLM(model='qwen3:4b')

result = model.invoke(input='你是谁？你能做什么？')

print(result)
'''