from langchain_community.document_loaders import PyPDFLoader

##使用到的文档是：data文件夹下的pdf1.pdf文件【该文件没有设置密码】
pdf_loader = PyPDFLoader( #解析
    file_path = "./data/pdf1.pdf",
    mode = "page", #page模式，pdf文件的每一页就是一个Document对象。这个参数不填默认是page。
    #password=""
)

documents = pdf_loader.load()
print(len(documents))
print(documents)
for doc in documents:
    print("-"*40)
    print(doc)
    print("-" * 40)

print("\n\n\n\n")
print("以上是一次性加载，以下是懒加载：") #pdf文件有23页，算比较大，可以使用lazy_load()方法
i=0
for doc in pdf_loader.lazy_load():
    i += 1
    print("-" * 40)
    print(doc)
    print("-" * 40)
print(f"使用懒加载方式，一共加载了{i}次，即有{i}个Document对象")