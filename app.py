import streamlit as st
import ollama

MODEL = "gemma3:1b"

st.title("MODel Testing with Ollama")
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def generate_response():
    response = ollama.chat(model=MODEL, messages=st.session_state.messages, stream=True)
    for chunk in response:
        token = chunk["message"]["content"]
        st.session_state["full_message"] += token
        yield token

if prompt := st.chat_input("Enter your prompt here"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    st.session_state["full_message"] = ""
    with st.chat_message("assistant"):
        stream = generate_response()
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
