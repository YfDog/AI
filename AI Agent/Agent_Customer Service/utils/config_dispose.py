'''
工程项目里正经使用配置文件用yaml格式:
key:value
需要导入yaml包
'''
'''
本文件要处理四个配置：
各个函数加载对应的yaml配置文件：
rag知识库相关配置
chroma数据库相关配置
prompt提示词切换相关配置
agent智能体相关配置
'''

import yaml
from utils.path_tool import get_abs_path

rag_config_path = get_abs_path("config/rag.yml")
chroma_config_path = get_abs_path("config/chroma.yml")
prompts_config_path = get_abs_path("config/prompts.yml")
agent_config_path = get_abs_path("config/agent.yml")

def load_rag_config(config_path:str=rag_config_path, encoding:str="utf-8"): #参数里设置了默认值，使用时如果不传参数就按默认值来
    with open(config_path,"r",encoding="utf-8") as f:
        return yaml.load(f,Loader=yaml.FullLoader)

def load_chroma_config(config_path:str=chroma_config_path,encoding:str="utf-8"):
    with open(config_path,"r",encoding="utf-8") as f:
        return yaml.load(f,Loader=yaml.FullLoader)

def load_prompts_config(config_path:str=prompts_config_path,encoding:str="utf-8"):
    with open(config_path,"r",encoding="utf-8") as f:
        return yaml.load(f,Loader=yaml.FullLoader)

def load_agent_config(config_path:str=agent_config_path,encoding:str="utf-8"):
    with open(config_path,"r",encoding="utf-8") as f:
        return yaml.load(f,Loader=yaml.FullLoader)

#快捷获取
rag_config = load_rag_config()
chroma_config = load_chroma_config()
prompts_config = load_prompts_config()
agent_config = load_agent_config()


# if __name__ == '__main__':
#     print(rag_config["chat_model"])
#       

