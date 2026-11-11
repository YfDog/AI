from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

##所用到的文件是：data文件夹下的Python基础语法.txt文件
text_loader = TextLoader( #解析
    "./data/Python基础语法.txt",
    encoding="utf-8",
)

document = text_loader.load() #加载。TextLoader加载的文档无论文档大小，返回的都只有一个Document对象
print(document)
print(len(document))  #长度是1，意味着只有1个Document对象

splitter = RecursiveCharacterTextSplitter(
     chunk_size = 500,    #将文本进行分段，每段的最大字符数
    chunk_overlap = 50,   #段与段之间允许的最大重叠字符数，这个参数是为了保证分段的语义完整性
    separators = ["\n\n", "\n", "。", "？", "！", ".", "?", "!", " ", ""],  #RecursiveCharacterTextSplitter类是按自然段落分割文档，常见的自然段落分割符有这些，还有的要根据具体的文档进行separators参数的设置
    length_function = len,  #用什么方法/函数统计字符数，这里用的是Python自带的len
)

doc_split_documents = splitter.split_documents(document)
print(doc_split_documents)
print(len(doc_split_documents))  #56,也就是将一个Document对象分割成了56个Document对象
for doc in doc_split_documents:
    print("-"*20)
    print(doc)
    print("-" * 20)




