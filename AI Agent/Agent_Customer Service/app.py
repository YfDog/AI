import streamlit as st
from agent.realization_agent import RealizationAgent


st.title("扫地机器人智能客服")
st.divider()

if "agent" not in st.session_state:
    st.session_state["agent"] = RealizationAgent()

if "message" not in st.session_state:
    st.session_state["message"] = []

for message_dict in st.session_state["message"]:
    st.chat_message(message_dict["role"]).write(message_dict["content"])

#提供输入框，供用户输入提示词
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","content":prompt})

    response_messages = []
    with st.spinner("智能客服思考中..."):
        responses_stream = st.session_state["agent"].execute_agent(prompt)

        def capture(responses,store):
            for res in responses:
                store.append(res)  #res是一小段的文字
                for char in res:
                    yield char

        st.chat_message("ai").write_stream(capture(responses_stream,response_messages))
        st.session_state["message"].append({"role": "ai", "content": response_messages[-1]})
        st.rerun()