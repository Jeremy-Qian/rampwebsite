import streamlit as st

# 从secrets中获取正确的code
correct_code = st.secrets["code"]
st.session_state['logged_in'] = False
@st.dialog
def login():
    # 创建密码输入框
    user_input_code = st.text_input("请输入登录密码", type="password")

    # 验证用户输入的code
    if user_input_code == correct_code:
        st.success("密码正确，欢迎登录！")
        st.session_state['logged_in'] = True
    else:
        st.error("密码输入错误，请重新输入。")
if not st.session_state['logged_in']:
    login()

if st.session_state['logged_in']:
    st.title("欢迎使用 Streamlit 应用")
    st.write("这是一个受保护的页面，只有输入正确的密码才能访问。")
    st.write("你可以在这里放置你的应用程序内容。")