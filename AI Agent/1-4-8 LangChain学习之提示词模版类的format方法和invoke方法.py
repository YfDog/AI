from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
from langchain_core.prompts import ChatPromptTemplate

'''
-> : 翻译为继承于/继承自
继承关系：

PromptTemplate -> StringPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable
FewShotPromptTemplate -> StringPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable
ChatPromptTemplate -> BaseChatPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable
'''
#下面用代码实际跑一下format方法和invoke方法
#format方法
prompt_template = PromptTemplate.from_template("我的邻居姓：{lastname}，她养了宠物，宠物是{category}")
prompt_01 = prompt_template.format(lastname="王",category="狗")
print(prompt_01)
print("format方法返回的是字符串类型：",type(prompt_01))
#invoke方法
prompt_02 = prompt_template.invoke({"lastname":"张","category":"猫"})
print(prompt_02)
print("invoke方法返回的是StringPromptValue类型：",type(prompt_02))


'''
PromptTemplate类、FewShotPromptTemplate类、ChatPromptTemplate类都有共同的最高级别父类Runnable。
PromptTemplate、FewShotPromptTemplate、ChatPromptTemplate都继承自它们共同的父类：BasePromptTemplate，
而BasePromptTemplate类定义了format方法。
BasePromptTemplate类继承自它的父类Runnable，而Runnable类定义了invoke方法。
所以PromptTemplate、FewShotPromptTemplate、ChatPromptTemplate这三个类既能使用invoke方法也能使用format方法。
'''
