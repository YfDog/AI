import hashlib
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from utils.logger_handler import logger
from utils.config_dispose import chroma_config
from utils.path_tool import get_abs_path
'''
检查文件md5值流程【check_file_md5函数流程】：
有该文件md5值 -> 打开存储各文件md5值的存储文件 -> 取出每一行md5值比对 -> 查到有一模一样的值 -> 该文件被处理过，返回False（处理：加载->分割->向量化->存储入库）
                                                                -> 没有一模一样的值 -> 该文件未被处理过，返回True（处理：加载->分割->向量化->存储入库）
执行检查流程前，要确保存储各文件md5值的存储文件存在 -> 若不存在，则创建存储文件，返回False[存储md5的文件都没有，那我这份文件的md5值一定没有被处理过，返回False]
                                              -> 若存在，则打开存储文件执行流程
'''

def get_file_md5(file_path:str):  #获取文件的md5值（md5值是32位16进制的）
    #先处理一下两个可能会出现的错误情况
    #文件路径不存在
    if not os.path.exists(file_path):
        logger.error(f"[md5计算]{file_path}路径不存在") #输出到日志里
        return
    #路径终点不是文件
    if not os.path.isfile(file_path):
        logger.error(f"[md5计算]路径{file_path}的终点不是文件")
        return

    md5_calculator = hashlib.md5()

    chunk_size = 4096   #4KB分片，若文件过大10GB 100GB，一次性加载内存放不下，文件要分片处理，一片一片把文件拿过来去更新md5，最终算出完整文件的md5

    try:
        with open(file_path,"rb") as f: #对文件分片计算md5值必须二进制读取
            chunk = f.read(chunk_size)
            while chunk:
                md5_calculator.update(chunk)
                chunk = f.read(chunk_size)

            md5_hex = md5_calculator.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"[md5计算]计算文件{file_path}的md5失败，详细信息：{str(e)}")
        return None

def check_file_md5(md5_value:str):
    #首先要有存储各个文件md5值的存储文件，有了这个存储文件，才能检查md5_for_check这个参数的md5值有没有重复的
    #先判断存储文件是否存在
    #reture False  这个文件的md5值不在md5存储文件里，证明这个文件没有被处理【处理：加载文档->文档分割->向量化->存储】
    #reture True  这个文件的md5值在md5存储文件里，证明这个文件已经被处理过，不能再重复处理【处理：加载文档->文档分割->向量化->存储】
    md5_store_file = get_abs_path(chroma_config["md5_store_file"])
    if not os.path.exists(md5_store_file):
        #创建存储文件
        open(md5_store_file,"w",encoding="utf-8").close()
        return False #存储md5的文件都没有，那我这份文件的md5值一定没有被处理过，返回False

    with open(md5_store_file,"r",encoding="utf-8") as f:
        for line in f.readlines():
            if line == md5_value:
                return True
        return False

def store_file_md5(md5_value):
    md5_store_file = get_abs_path(chroma_config["md5_store_file"])
    with open(md5_store_file,"a",encoding="utf-8") as f:
        f.write(md5_value+"\n")


def pdf_loader(file_path:str,password=None)->list[Document]:
    return PyPDFLoader(file_path,password).load()

def txt_loader(file_path:str) -> list[Document]:
    return TextLoader(file_path,encoding="utf-8").load()

def get_file_documents(file_path: str): #初步获取，后续还要根据每一个document的大小决定是否再分割
    if file_path.endswith("txt"):
        return txt_loader(file_path)
    if file_path.endswith("pdf"):
        return pdf_loader(file_path)
    return []


def dir_list_with_allowed_type(dir_path:str,allowed_type:tuple[str]): #返回文件夹内的文件列表【允许的文件后缀】，得到的是文件路径
    files_path = []

    #看文件夹里有哪些文件【允许的文件后缀】，所以需要判断给的路径终点是不是文件夹
    if not os.path.isdir(dir_path):
        logger.error(f"[dir_list_with_allowed_type]给的{dir_path}路径终点不是文件夹")
        return allowed_type

    for fn in os.listdir(dir_path):
        if fn.endswith(allowed_type):
            files_path.append(os.path.join(dir_path,fn))

    return tuple(files_path) #强制类型转换，转为元组，不可更改


# if __name__ == '__main__':
#     print(dir_list_with_allowed_type("D:\AI Study\AI Agent\Agent_Customer Service\Data",("txt","pdf")))