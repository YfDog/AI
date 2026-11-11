from langchain_community.document_loaders import CSVLoader
#所用到的文件是：data文件夹下的stu.csv文件
csv_loader = CSVLoader(file_path="./data/stu.csv",
                       encoding="utf-8", #windows系统下， 默认是用GBK编码打开文件，而文件是utf-8编码，因此要注明读写文件的编码方式，防止出错。
                       ) #解析

documents_csv = csv_loader.load() #加载：load()方法是一次性加载

print(documents_csv,type(documents_csv)) #使用load()方法加载csv文件，返回的是：list[document对象，document对象，document对象，...]
                                         #documents_csv对象的类型是list
print("\n"+"上面是拿到csv文件的返回结果后打印出的全部内容，下面是从返回的数据中一个个取出document对象：")
for doc in documents_csv:
    print(doc,type(doc)) #doc对象的类型是Document

print("\n"+"以下是懒加载方式，也就是分批流式加载：")
for document_lazy_csv in csv_loader.lazy_load(): #lazy_load()方法返回的是：迭代器[Document，Document，...]，只不过不是一次性加载过来，而是流式加载
    print(document_lazy_csv)

