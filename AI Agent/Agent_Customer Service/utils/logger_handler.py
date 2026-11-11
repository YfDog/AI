import logging
from datetime import datetime
from utils.path_tool import get_abs_path
import os

#日志保存的根目录(绝对路径)
LOG_ROOT = get_abs_path("log_store")

#创建目录。这一步也是确保日志的目录存在
os.makedirs(LOG_ROOT,exist_ok=True)

#日志的格式
DEFAULT_LOG_FORMAT = logging.Formatter(
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)#日志格式为：时间 - 日志名字 - 日志级别 - 文件名:该文件第几行 - 日志正文信息

def get_logger(
        name:str = "logger_agent",         #日志记录器叫什么名字
        console_level:int = logging.INFO,  #级别设置为INFO，级别等于大于INFO的才会在控制台输出
        file_level:int = logging.DEBUG,    #级别设置为DEBUG，级别等于大于DEBUG的才会写入文件
        log_file = None,
) -> logging.Logger: #返回的是logging.Logger对象，拿到这个对象后就能调用info()方法、debug()方法等
    '''获得一个日志记录器。这个日志记录器有两个handler：往控制台输出记录handler和往文件记录handler'''
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    #避免重复添加Handler
    if logger.handlers:
        return logger

    #控制台handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(console_handler)

    #文件handler
    #创建文件handler前要有日志文件的存放路径
    if not log_file:
        log_file = os.path.join(LOG_ROOT,f"{name}_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler = logging.FileHandler(log_file,encoding="utf-8") #要传日志的存放文件路径
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(file_handler)

    return logger

#快捷获取logger。其他文件使用logger先导包from logger_handler import logger或者from utils.logger_handler import logger再 logger. 这样去使用
logger = get_logger()

# if __name__ == '__main__':
#     logger.debug("调试日志")
#     logger.info("信息日志")
#     logger.warning("警告日志")
#     logger.error("错误日志")

