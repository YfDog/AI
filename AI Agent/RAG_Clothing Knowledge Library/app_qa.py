from Tools.scripts.dutree import store

from rag import RagService
import config
import streamlit as st
import time

st.title("智能客服")

st.divider()  #分隔符

#在页面下方提供一个用户输入栏
prompt = st.chat_input()

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role":"assistant","content":"你好，有什么可以帮助你的？"}
    ]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

if prompt:
    #在页面输出用户的提问
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role":"user","content":prompt})
    store = [] #列表里是若干个 字符串
    with st.spinner("AI思考中。。。"):
        # responses = st.session_state["rag"].chain.invoke({"user_input":prompt},config.session_id_config)
        # st.chat_message("ai").write(responses)
        # st.session_state["messages"].append({"role": "ai", "content": responses})
        #以上方式AI回复是一次性全部输出，用户体验一般，下面改为流式输出
        responses_stream = st.session_state["rag"].chain.stream({"user_input":prompt},config.session_id_config)
        def dispose(responses,store):
            for res in responses:
                store.append(res)
                yield res

        st.chat_message("ai").write_stream(dispose(responses_stream,store))
        st.session_state["messages"].append({"role":"ai","content":"".join(store)})


#模型的流式输出的返回的是一个迭代器
#append({"role":"ai","content":responses_stream}) 中的responses_stream是迭代器，不符合输入类型要求，模型回复保存不下来。要求的输入是字符串类型

