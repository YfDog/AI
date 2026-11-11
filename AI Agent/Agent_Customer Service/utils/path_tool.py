'''
为整个工程提供统一的绝对路径
工程名：Agent_Customer Service
相对路径在解析时万一要出错会找不到路径对应的文件或数据，到时候比较麻烦
'''
import os

def get_project_root_path()->str:
    '''获取工程目录，工程名为：Agent_Customer Service'''
    '''工程Agent_Customer Service所在目录为：D:\AI Study\AI Agent\Agent_Customer Service（该函数要获取的就是这个路径）'''
    #先获取当前文件path_tool.py的绝对路径
    current_file_path = os.path.abspath(__file__)
    #再获取当前文件所在的文件夹的绝对路径
    current_dir_path = os.path.dirname(current_file_path)
    #再获取当前文件所在的文件夹的文件夹的绝对路径，这就是工程的绝对路径
    project_path= os.path.dirname(current_dir_path)

    return project_path #这是绝对路径

def get_abs_path(relative_path:str)->str: #示例：print(get_abs_path("utils/path_tool.py"))
    '''传入相对路径，拼接成绝对路径'''
    return os.path.join(get_project_root_path(),relative_path)





