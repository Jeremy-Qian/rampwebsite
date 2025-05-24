import streamlit as st  
import time  
from jerechat import *

st.set_page_config(page_title="Chat App", layout="wide", initial_sidebar_state="collapsed")  
st.title("Let's Chat!")  

if "messages" not in st.session_state:  
    st.session_state.messages = []  

for msg in st.session_state.messages:  
    with st.chat_message(msg["role"]):  
        st.write(msg["content"])  

prompt = st.chat_input("Say something...")  

if prompt:  
    st.session_state.messages.append({"role": "user", "content": prompt})  
    with st.chat_message("user"):  
        st.write(prompt)  

    first_time = time.time()
    bot_response = generate_response(prompt)
    second_time = time.time()
    elapsed_time = second_time - first_time
    elapse_text = f"> Thought for {elapsed_time:.2f} seconds."
    st.session_state.messages.append({"role": "bot", "content": elapse_text + bot_response})  
    with st.chat_message("bot"):  
        st.write(bot_response)  