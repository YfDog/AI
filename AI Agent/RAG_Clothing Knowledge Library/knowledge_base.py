'''
知识库更新服务：
1.文本内容的md5值 检查、保存、文本内容转md5值
2.文本内容向量化存入向量数据库中
'''
import hashlib
import os.path

from datetime import datetime
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config

def check_md5(md5_str:str):
    '''检查这个md5有没有被处理过'''
    '''这个md5被处理过了，代表这份文件数据已经被处理过了，即该文件数据在知识库已经存在'''
    '''怎么知道文件内容所对应的md5有没有被处理过？-可以在保存md5值的文件里找，找到了一样的值，说明该md5已被处理过
                                                                没找到，说明该md5值是新的，未被处理过'''
    '''规定：return False  表示md5没有处理过
            return True   表示md5已经处理过了'''
    '''另外，文件应该存储在哪里，数值应该多大最好的方式是在配置文件里配置好写好'''
    if not os.path.exists(config.path):
        open(config.path,"w",encoding="utf-8").close()
        return False
    else:
        for line in open(config.path,"r",encoding="utf-8").readlines():
            line=line.strip()   #strip()方法用于处理字符串前后的空格和回车
            if line == md5_str:
                return True
        return False

def store_md5(md5_str:str): #课程中函数名为：save_md5
    '''将文件内容所对应的md5值保存到text文件'''
    with open(config.path,"a",encoding="utf-8") as f: # "a"是追加写
        f.write(md5_str+"\n")


def string_to_md5(input_str:str,encoding="utf-8"): # 课程中函数名为：get_string_md5
    '''将文件内容转为md5值'''
    '''要先将传进来的字符串还原为二进制，用utf-8编码去还原'''
    bytes = input_str.encode(encoding="utf-8")

    md5_calculator = hashlib.md5()  #创建md5对象，用于计算md5值的
    md5_calculator.update(bytes)    #往md5对象放数据，计算
    md5_hex = md5_calculator.hexdigest()  #取出32位16进制小写的md5串

    return md5_hex


class KnowledgeBaseService(object):
    def __init__(self):

        os.makedirs(config.chroma_persist_directory,exist_ok=True)#一般情况下，我们希望数据库的文件夹路径是存在的，所以先创建一个数据库的存放路径
        self.chroma = Chroma(
            collection_name = config.chroma_collection_name ,  #数据库表名
            embedding_function = OllamaEmbeddings(model = config.embedding_model),
            persist_directory = config.chroma_persist_directory  #数据库的存放路径
        )#向量存储的数据库实例（chroma数据库对象）

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size = config.spliter_chunk_size,        #将文本分割成一段一段的，每一段文本最大的字符数
            chunk_overlap = config.spliter_chunk_overlap,  #每段之间可重叠的最大字符数
            separators = config.separators,
            length_function = len,
        )   #文本分割器对象

    def _to_vector_store(self,data:str,filename): #课程中函数名为：upload_by_str
        '''文本内容向量化，存入数据库里'''
        #先检查这份文本之前有没有被处理过，也就是检查文本的md5值。
        md5_hex = string_to_md5(data)
        if check_md5(md5_hex):
            return "[跳过]内容已经上传过了"
        if len(data) > config.split_threshold:
            knowledge_chunk:list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunk = [data] #与上面的knowledge_chunk格式统一

        metadata = { #metadata 元数据，表明数据来源是？数据的操作员是？等等跟这份数据有关的原始信息
            "source":filename,
            "create_time":datetime.now().strftime("%Y-%M-%d %H:%M:%S"), #时间格式形如：2025-01-01 10:00:00
            "operator":"张三"
        }

        self.chroma.add_texts( #这个函数一执行，文本内容就会被向量化并且存储到数据库里了
            knowledge_chunk,
            metadatas = [metadata for _ in knowledge_chunk] #knowledge_chunk里的每一个数据的来源都是metadata里的信息
        )

        store_md5(md5_hex)

        return "[成功]文档内容成功上传至知识库中"

# if __name__ == '__main__':
    # r1 = string_to_md5("张三李四王五")
    # r2 = string_to_md5("张三李四王五")
    # r3 = string_to_md5("张三李四王五林七")
    # print(r1)
    # print(r2)
    # print(r3)
    # print(check_md5(r1))
    # store_md5(r1)
    # print(check_md5(r2))

    #以上是对三个功能函数：check_md5、store_md5、string_to_md5的测试，看看功能是否正常执行
    #这三个功能函数是为KnowledgeBaseService类的具体实现服务的
    #以下是对KnowledgeBaseService类的测试

    # knowledge_service = KnowledgeBaseService()
    # result = knowledge_service._to_vector_store("张三家住在李四家旁边，王五家住在陈六家上面，李四家住在王五家旁边，你知道他们的方位示意图怎么画吗？",
    #                                    "小学生思维训练")
    # print(result)