from langchain_community.document_loaders import JSONLoader

##所用到的文件是：data文件夹下的stus.json文件【json数组】
json_loader = JSONLoader(  #解析
    file_path = "./data/stus.json",
    jq_schema = ".[].name",
)

document = json_loader.load()
print(document)

