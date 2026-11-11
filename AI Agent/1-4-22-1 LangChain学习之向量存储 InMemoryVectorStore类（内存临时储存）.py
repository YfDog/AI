'''
1.有一个文档，先将文档加载过来，需要文档加载器
2.判断是否需要分割文档
3.文档内容转向量
4.存入向量库【向量库常用的3个操作：添加、删除、相似度搜索】
'''
from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore    # InMemoryVectorStore类，向量在内存中存储，属于临时储存。程序或电脑一关闭数据就没了。

##使用到的文档是：data文件夹下的info.csv文件
csv_loader = CSVLoader(
    file_path="./data/info.csv",
    encoding="utf-8",
    source_column="source", #source_column参数选择某一列作为数据的来源。这个参数不填数据来源默认是文件路径
)
documents = csv_loader.load() #CSVLoader加载文档，会对csv文件除表头外每一行数据划为Document对象，若该csv文件【除去表头】有10行数据，返回的列表里会有10个Document对象。
print(documents)
print(len(documents))

vector_store = InMemoryVectorStore(
    embedding =  DashScopeEmbeddings()
)
'''
下面是关于向量存储的三个方法：
add_document() 新增
delete() 删除
similarity_search() 相似度搜索
'''
add_store = vector_store.add_documents(
    documents = documents,  #添加哪个文档？ 参数输入类型是：list[Document,Document,Document,...]
    ids = ["id"+str(i) for i in range(1,len(documents)+1) ],  #给添加的文档标注id。参数输入的类型是：list[str,str,str,...]
                                                              #期望的id形如：id1、id2、id3......
)
print("文档的id序列为：",add_store)

del_docs = vector_store.delete(["id1","id2"])  #删除向量数据库里的向量【由文档内容转的向量】。删除时给出对应的id号
print("经删除操作后的文档的id序列为：",add_store)
'''
`add_store` 是**add_documents 返回的、新增文档的 id 列表**，它是一个普通 Python 列表，**不会自动跟着向量库的删除操作变化**！
`add_store` 只是当时添加成功的 id 快照，**不是向量数据库实时状态**
想打印出向量数据库里的id和对应内容，到时候可以问一下AI软件
'''

return_result = vector_store.similarity_search( #相似度搜索。先将用户的问题转为向量，再去向量数据库匹配，匹配完成返回结果
    "python真的简单易学嘛?" ,  #query查询
    3   #要几个结果
)
print("经过文档检索后的回复：")
i=0
for res in return_result:
    i+=1
    print(f"第{i}个回复：",res)

