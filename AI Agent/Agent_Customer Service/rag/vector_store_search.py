from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.config_dispose import chroma_config
from model.factory import embedding_model
from utils.file_dispose import txt_loader, pdf_loader, dir_list_with_allowed_type, get_file_md5, check_file_md5, \
    get_file_documents, store_file_md5
from utils.logger_handler import logger
from utils.path_tool import get_abs_path
'''
实现本文件的VectorStoreSearchService类之前，做了以下前置工作：
1.chroma.yml文件里 参数配置【D:\AI Study\AI Agent\Agent_Customer Service\config\chroma.yml】
2.factory.py文件里 编写生成模型实例的代码【D:\AI Study\AI Agent\Agent_Customer Service\model\factory.py】
以上前置工作做好后，开始编写本文件的VectorStoreSearchService类
    -类成员：self.chroma_vector_store [获得chroma数据库对象，用于向量化和存储入库]
            self.spliter             [获得文本分割器，用于将初步加载的Document进行分割]
    -类方法：get_retriever()          [该方法获得可入链的检索器]
            load_split_documents()   [该方法初步加载文档，再进行分割->向量化->存储入库](最后还要把文件的md5值保存起来)
'''


class VectorStoreSearchService(object):
    def __init__(self):
        self.chroma_vector_store = Chroma(
            collection_name = chroma_config["collection_name"],
            embedding_function = embedding_model,
            persist_directory = get_abs_path(chroma_config["persist_directory"]) #chroma_config["persist_directory"],这样写是相对路径
            #我们希望数据库的存储路径是D:\AI Study\AI Agent\Agent_Customer Service\chroma_db  chroma_db是文件夹
            #而不是在相对路径下：chroma_db。也就是最终在D:\AI Study\AI Agent\Agent_Customer Service\rag\chroma_db下
        )

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size = chroma_config["chunk_size"],
            chunk_overlap = chroma_config["chunk_overlap"],
            separators = chroma_config["separators"],
            length_function=len,
        )

    def get_retriever(self):
        retriever = self.chroma_vector_store.as_retriever(search_kwargs={"k":chroma_config["k"]})
        return retriever

    def load_split_documents(self):
        #先获得知识库的文件，多个文件就是最终获得tuple[str]，元组里是文件的绝对文件路径
        allow_file_list:tuple[str] = dir_list_with_allowed_type(  #得到的是列表，列表里是一个个文件路径(字符串形式)，绝对路径
            get_abs_path(chroma_config["data_path"]),
            tuple(chroma_config["allow_knowledge_file_type"])
        )

        for fp in allow_file_list:
            md5 = get_file_md5(fp)
            if check_file_md5(md5):
                logger.info(f"[检查文件MD5]{fp}文件已经在知识库中，跳过")
                continue #本轮循环结束
            try:
                no_split_document:list[Document] = get_file_documents(fp)

                if not no_split_document:
                    logger.warning(f"[加载文档]{fp}文件里没有文本内容，跳过")
                    continue

                already_split_documents = self.spliter.split_documents(no_split_document)

                if not already_split_documents:
                    logger.warning(f"[加载文档]{fp}被分片后没有有效文本内容，跳过")
                    continue

                #存入数据库（chroma数据库自带向量化功能并存储入库）
                self.chroma_vector_store.add_documents(already_split_documents)

                #存储该文件md5值
                store_file_md5(md5)
                logger.info(f"[加载知识库]{fp}的内容加载成功，已成功存储进数据库里")
            except Exception as e:
                logger.error(f"[加载知识库]{fp}的内容加载失败，详细信息：{str(e)}",exc_info=True) #exc_info=True会记录详细的报错堆栈，如果为False只记录报错信息本身


# if __name__ == '__main__':
#     vector_store_service = VectorStoreSearchService()
#     vector_store_service.load_split_documents()
#     retriever = vector_store_service.get_retriever()
#
#     search_result = retriever.invoke("迷路")
#     for sres in search_result:
#         print(sres.page_content)

























