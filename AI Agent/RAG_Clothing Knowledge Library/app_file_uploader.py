'''
使用Streamlit框架开发WEB网页
该网页用于将文档上传
需要pip install streamlit
'''
#streamlit框架的特点：只要web页面的元素发生变化，.py文件的代码会从上到下重新跑，
#这样的特性有比较大的问题，状态是无法保存的，只要web页面发生变化，代码重新跑，状态也会直接变成初始状态。
#streamlit官方提供了一种解决方法：st.session_state，是一个{字典}

import streamlit as st
from knowledge_base import KnowledgeBaseService

st.title("知识库更新服务") #title 一级标题

upload_file = st.file_uploader(
    label = "请上传TXT文件",
    type = ['txt'],
    accept_multiple_files = False, #参数accept_multiple_files表示是否接受多文本上传，填False：一次只能上传一个文件
)
# if "file_upload_count" not in st.session_state: #"file_upload_count" 这个键如果不在session_state这个字典里就进入判断
#     st.session_state["file_upload_count"] = 0
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()  #通过session_state字典的键去得到KnowledgeBaseService类对象，再通过调用方法去存储文本内容

if upload_file is not None:
    #提取文件信息
    file_name = upload_file.name
    file_type = upload_file.type
    file_size = upload_file.size  #单位是字节 B

    #展示文件基础信息
    st.subheader("文件信息：")
    st.write(f"文件名：{file_name}")
    st.write(f"文件类型：{file_type}")
    st.write(f"文件大小：{file_size/1024:.2f}KB")  #file_size/1024 是KB单位；（file_size/1024）:.2f 数字保留小数点后两位

    #获取文件内容
    #st.subheader("文件内容：")
    content = upload_file.getvalue().decode("utf-8")
    #st.write(content) #长文本推荐用 `st.text_area` 预览，不然会很卡

    result = st.session_state["service"]._to_vector_store(content,file_name)
    if result == "[成功]文档内容成功上传至知识库中":
        st.success(f"✅ {result}")
    if result == "[跳过]内容已经上传过了":
        st.error(f"❌ {result}")


    # st.session_state["file_upload_count"] += 1

# print(f'上传了{st.session_state["file_upload_count"]}个文件')