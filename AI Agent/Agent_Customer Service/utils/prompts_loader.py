from utils.path_tool import get_abs_path
from utils.config_dispose import prompts_config
from utils.logger_handler import logger

def load_system_main_prompt():
    try:
        prompt_path = get_abs_path(prompts_config["main_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_system_main_prompt]在yaml文件中没有main_prompt_path的配置项")
        raise e

    try:
        return open(prompt_path,"r",encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_system_main_prompt]解析读取{prompt_path}的内容(系统主提示词)出错，详细信息：{str(e)}")
        raise e


def load_rag_summarize_prompt():
    try:
        prompt_path = get_abs_path(prompts_config["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_rag_summarize_prompt]在yaml文件中没有rag_summarize_prompt_path的配置项")
        raise e

    try:
        return open(prompt_path,"r",encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_rag_summarize_prompt]解析读取{prompt_path}的内容(RAG知识库总结提示词)出错，详细信息：{str(e)}")
        raise e

def load_report_prompt():
    try:
        prompt_path = get_abs_path(prompts_config["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_report_prompt]在yaml文件中没有report_prompt_path的配置项")
        raise e

    try:
        return open(prompt_path,"r",encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_report_prompt]解析读取{prompt_path}的内容(报告生成提示词)出错，详细信息：{str(e)}")
        raise e  #把异常抛出，交给调用该函数的上层代码

# if __name__ == '__main__':
#     print(load_report_prompt())