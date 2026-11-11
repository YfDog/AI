#使用JSONLoader需要jq包，要在命令行运行pip install jq命令
from langchain_community.document_loaders import JSONLoader #文档加载器的目的最终是要把各种各样的文档处理成一个个Document对象，方便后续向量化。


##所用到的文件是：data文件夹下的stu.json文件【单个json对象】
json_loader = JSONLoader( #解析
    file_path = "./data/stu.json",
    jq_schema =".",  #根据jq的语法抽取想要的数据，这里抽取的是json的name信息，最终结果是张三
    text_content = False,  #jq_schema ="."，抽取的数据是dict，不是字符串类型，这里填false，告知JSONLoader，我要抽取的内容不是字符串，不然会报错。
                           #像jq_schema=".name",这种情况，text_content这个参数可以没有。
)
#jq_schema=".name",运行结果是：[Document(metadata={'source': 'D:\\AI Study\\AI Agent\\data\\stu.json', 'seq_num': 1}, page_content='张三')]
#jq_schema=".other.addr",运行结果是：[Document(metadata={'source': 'D:\\AI Study\\AI Agent\\data\\stu.json', 'seq_num': 1}, page_content='深圳')]
#jq_schema =".",按理来说应该是整个json对象，但是会报错，Document对象里的page_content键期望的值是字符串，但返回的是字典dict，
#解决办法就是添加一个text_content=False的参数

documents = json_loader.load()
print(documents)