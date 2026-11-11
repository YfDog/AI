'''
本文件的RagService类是供Agent智能体使用的工具。
将用户提问和根据用户提问检索到的参考资料一并交给模型，模型生成简洁准确的概括回答
'''
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from model.factory import chat_model
from rag.vector_store_search import VectorStoreSearchService

from utils.prompts_loader import load_rag_summarize_prompt

def print_prompt(completion_prompt):
    print("以下是完整提示词：")
    print(completion_prompt.to_string())
    print("-"*20)
    return completion_prompt

class RagService(object):  #将用户提问和根据用户提问检索到的参考资料一并交给模型，模型生成简洁准确的概括回答
   def __init__(self):
       self.chroma_vector_store_search = VectorStoreSearchService()  #self.chroma_vector_store_search是为self.retriever服务的

       self.retriever = self.chroma_vector_store_search.get_retriever() #这个retriever是vector_store_search.py文件下VectorStoreSearchService类的get_retriever()方法的实例，所以self.retriever写在类成员里

       self.prompt_text_for_template = load_rag_summarize_prompt()  #self.prompt_text_for_template是为self.prompt_template服务的

       self.prompt_template = PromptTemplate.from_template(self.prompt_text_for_template)

       self.model = chat_model

       self.chain = self._init_chain()

   def _init_chain(self):
         chain = self.prompt_template | print_prompt | self.model | StrOutputParser()
         return chain

   def execute_retriever(self,query:str)->list[Document]:
       return self.retriever.invoke(query)

   def execute_rag(self,query:str)->str: #核心用法
       content = self.execute_retriever(query)

       reference_content = ""
       counter=0
       for con in content:
           counter += 1
       reference_content += f"【参考资料{counter}】：正文：{con.page_content} \n 来源：{con.metadata}\n"

       return self.chain.invoke(
           {
               "input":query,
               "context":reference_content
           }
       )

# if __name__ == '__main__':
#     print(RagService().execute_rag("60平方米的屋子适合用什么扫地机器人"))




