#search_service.py，课程中的文件名是：vector_stores.py
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
import config

class SearchServiceRetriever(object):
    def __init__(self):
        self.search_service = Chroma(  #self.search_service，课程的名字是self.vector_service
            collection_name = config.chroma_collection_name,
            embedding_function = OllamaEmbeddings(model = config.embedding_model), # =的右边直接写config.embedding_model是错误的
            persist_directory = config.chroma_persist_directory
        )

    def get_retriever(self):
        '''返回可入链的检索器'''
        return self.search_service.as_retriever(search_kwargs={"k":config.search_result_maxnum})

# if __name__ == '__main__':  #测试
#     retriever = SearchServiceRetriever().get_retriever()
#     search_result = retriever.invoke("张三的身高169cm，体重126斤，请给张三推荐衣服尺码。")
#     print(search_result)
#     print(search_result[0].page_content)



