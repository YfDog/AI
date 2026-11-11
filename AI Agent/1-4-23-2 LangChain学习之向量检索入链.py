'''
用户提问到向量数据库检索，然后将用户提问与检索到的内容构建提示词去向模型提问，
因此最终的提示词是：用户提问+知识库检索到的内容。
'''
from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings

model = ChatTongyi(model="qwen3.7-max")

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system","以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料：{context}。"),
        ("user","用户提问：{input}"),
    ]
)

vector_store = InMemoryVectorStore(
    embedding = DashScopeEmbeddings(model="text-embedding-v4")
)
vector_texts = vector_store.add_texts( #准备知识库的资料
    ["减肥就是要少吃多练。","在减肥期间吃东西很重要，清淡少油控制卡路里摄入并运动起来。","跑步是很好的运动哦。"]
) #add_texts()方法用起来比较快捷

user_input = "我想减肥，我应该要怎么做？"  #准备用户的提问
#向量检索入链，核心要关注向量检索相关的类，比如内存临时数据库类：InMemoryVectorStore类
#InMemoryVectorStore类不是Runnable接口的实例，无法直接入链
#不过，langchian中关于向量存储对象有一个方法：as_retriever()，向量存储对象引用这个方法可以返回Runnable接口类
retriever = vector_store.as_retriever(search_kwargs={"k":2}) #search_kwargs参数的k是最多从向量数据库里得到几个参考
print(type(retriever)) #返回的结果是：VectorStoreRetriever，VectorStoreRetriever是Runnable接口的子类，retriever对象可以入链
'''
1.模型model
2.提示词模版prompt_template
3.向量数据库+数据库里的数据+as_retriever()方法处理 -> retriever
4.用户输入数据
以上准备好了后，我们设想chain链的组建为：先向量数据库检索，检索出的结果给提示词模版，形成完整提示词给到模型，模型输出回答
chain = retriever | prompt_template | model | StrOutputParser()
我们先来看前两个：
retriever：
     -输入：用户提问          str
     -输出：向量库的检索结果   list[Document]
prompt_template：
    -输入：用户提问+向量库的检索结果  dict
    -输出：完整的提示词            PromptValue
  
现在来分析一下这两个组件：
1.组件之间：前一个组件的输出要与后一个组件的输入类型对的上，
retriever的输出类型是list[Document]，而prompt_template的输入类型是dict，类型匹配不上
2.就算强制类型转换将list[Document]转为dict，
retriever的输出内容是向量库的检索结果，而prompt_template要的输入内容是用户提问+向量库的检索结果
前一个组件的输出内容与后一个组件需要的输入内容也匹配不上

以上，这种chain链的写法是不对的。需要改进。
下面是改进的代码写法：
'''
def print_prompt(completion_prompt):
    print("\n以下是完整提示词：")
    print(completion_prompt.to_string())
    return completion_prompt

def dispose_func(list_docs):
    if not list_docs:
        return "知识库没有相关参考资料"
    reference_text = "["
    for doc in list_docs:
        reference_text += doc.page_content
    reference_text += "]"
    return reference_text

#字典的顶级父类是Mapping，而Mapping类型是能入链的，因此字典也能入链
chain = {"context":retriever | dispose_func,  "input":RunnablePassthrough()} | prompt_template | print_prompt | model | StrOutputParser()

responses = chain.invoke(user_input)
print("以下是模型的回答：")
print(responses)
'''
invoke触发执行链，invoke的输入会给到chain链的第1个组件：{"context":retriever | dispose_func,  "input":RunnablePassthrough()}
而这个组件内部有两个组件：retriever和RunnablePassthrough
因此，输入实际是给了内部的这两个组件，而RunnablePassthrough是输入是什么，输出就是什么，输入是str是可以的
retriever规定的输入是str，所以invoke给了str类型的数据。

用户输入给到了向量检索，向量检索出参考资料list[Document]类型，送入dispose_func函数处理成list。
用户输入同时也给到了RunnablePassthrough()，RunnablePassthrough()能将invoke传进chain链的数据截取过来。"input"就获取了对应的数据。
'''



# result = vector_store.similarity_search(
#     user_input,
#     2,
# )
# reference_text = "[" #将知识库里检索到的内容处理一下，使其组装形成一个完整列表，检索到的内容在[]里
# for res in result:
#     reference_text += res.page_content
# reference_text += "]"
# print("这是在知识库检索的：",reference_text)
# '''
# 1.模型
# 2.提示词模版
# 3.向量数据库【参数设置文本转向量】
# 4.要存入数据库的具体数据
# 5.用户提问
# 6.相似度搜索
# 7.对搜索结果的处理
# 以上全部准备完成后可以构建链条了
# '''
# def print_prompt(completion_prompt):
#     print("\n以下是完整提示词：")
#     print(completion_prompt.to_string())
#     return completion_prompt
#
# chain = prompt_template |print_prompt| model | StrOutputParser()
#
# responses = chain.invoke({"context":reference_text,"input":user_input})
# print("\n以下是模型的回复：")
# print(responses)

