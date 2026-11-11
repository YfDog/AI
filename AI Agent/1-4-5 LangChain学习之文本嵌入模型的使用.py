from langchain_community.embeddings import DashScopeEmbeddings

embed = DashScopeEmbeddings() #括号内填写模型名称，若是括号内没写则默认是：text-embedding-v1

em_a = embed.embed_query("今天星期一")
em_b = embed.embed_documents(["今天星期六","今天星期三","今天周一"]) #列表形式可以存放好多个字符串

print(em_a)
print(em_b)

'''
不分开写，写在一块也是可以的
print(embed.embed_query("今天星期一"))
print(embed.embed_documents(["今天星期六","今天星期三","今天周一"]))
'''

'''
使用Oll ama本地模型的代码：
from langchain_ollama import OllamaEmbeddings

embed = OllamaEmbeddings(model="qwen3-embedding")

em_a = embed.embed_query("今天星期一")
em_b = embed.embed_documents(["今天星期天","今天星期四","今天周一"])

print(em_a)
print(em_b)
'''