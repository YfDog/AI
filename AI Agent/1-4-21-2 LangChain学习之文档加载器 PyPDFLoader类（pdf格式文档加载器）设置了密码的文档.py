from langchain_community.document_loaders import PyPDFLoader

##使用到的文档是：data文件夹下的pdf2.pdf文件【该文件设置了密码：itheima】
pdf_loader = PyPDFLoader( #解析
    file_path = "./data/pdf2.pdf",
    mode = "page", #page模式，pdf文件的每一页就是一个Document对象。这个参数不填默认是page。
    password="itheima"
)

documents = pdf_loader.load()
print(len(documents))
print(documents)
# for doc in documents:
#     print("-"*40)
#     print(doc)
#     print("-" * 40)