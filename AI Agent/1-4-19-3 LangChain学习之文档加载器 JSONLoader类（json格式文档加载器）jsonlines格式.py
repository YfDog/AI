from langchain_community.document_loaders import JSONLoader

#jsonlines格式的文件抽取数据方式比较灵活，不会可以问问AI软件
##所用到的文件是：data文件夹下的stu_json_lines.json文件【jsonlines格式】【jsonlines格式的文件：每一行都是单个json对象】
json_loader = JSONLoader(
    file_path="./data/stu_json_lines.json",
    jq_schema = ".name",
    #text_content=False,
    json_lines=True, #告知JSONLoader这是一个jsonlines格式的文件
)

documents = json_loader.load()
print(documents)

first_name = documents[0].page_content
print(first_name)