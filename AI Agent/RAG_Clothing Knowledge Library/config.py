#from langchain_ollama import OllamaEmbeddings
#knowledge_base.py
path = "./Data/MD5_data.text"  #check_md5函数  store_md5函数

chroma_collection_name = "RAG_Knowledge"        #KnowledgeBaseService类
embedding_model = "qwen3-embedding:0.6b"           #KnowledgeBaseService类，SearchServiceRetriever类【search_service.py】
chroma_persist_directory = "./chroma_db"        #KnowledgeBaseService类

spliter_chunk_size = 1000                       #KnowledgeBaseService类
spliter_chunk_overlap = 100                     #KnowledgeBaseService类
separators = ["\n\n","\n",".","?","!","。","？","！"," ",""]  #KnowledgeBaseService类

split_threshold = 1000         #KnowledgeBaseService类的_to_vector_store函数

#search_service.py
search_result_maxnum = 1  #向量检索最多返回的结果数量

#rag.py
chat_model = "qwen2.5:1.5b-instruct"

session_id_config = {
        "configurable": {"session_id": "admin_user"}
    }








