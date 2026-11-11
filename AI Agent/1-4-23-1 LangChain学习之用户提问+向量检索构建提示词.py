'''
用户提问到向量数据库检索，然后将用户提问与检索到的内容构建提示词去向模型提问，
因此最终的提示词是：用户提问+知识库检索到的内容。
'''
from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
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

result = vector_store.similarity_search(
    user_input,
    2,
)
reference_text = "[" #将知识库里检索到的内容处理一下，使其组装形成一个完整列表，检索到的内容在[]里
for res in result:
    reference_text += res.page_content
reference_text += "]"
print("这是在知识库检索的：",reference_text)
'''
1.模型
2.提示词模版
3.向量数据库【参数设置文本转向量】
4.要存入数据库的具体数据
5.用户提问
6.相似度搜索
7.对搜索结果的处理
以上全部准备完成后可以构建链条了
'''
def print_prompt(completion_prompt):
    print("\n以下是完整提示词：")
    print(completion_prompt.to_string())
    return completion_prompt

chain = prompt_template |print_prompt| model | StrOutputParser()

responses = chain.invoke({"context":reference_text,"input":user_input})
print("\n以下是模型的回复：")
print(responses)

