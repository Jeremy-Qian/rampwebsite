import streamlit as st
from time import sleep

# 初始化会话状态
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.role = None

# 登录函数
def login():
    st.header("Login")
    username = st.text_input("Username")
    KEY = st.text_input("KEY", type="password")
    if st.button("Log In"):
        # 假设这里从 secrets 获取用户信息
        users = st.secrets.get("users", {})
        if username in users and users[username]["KEY"] == KEY:
            st.session_state.user = username
            st.session_state.role = users[username]["role"]
            st.success("Successfully logged in!")
            st.markdown(f":rainbow[Welcome, {st.session_state.user}!]")
            with st.spinner("Redirecting to main page..."):
                sleep(1)
            st.rerun()
        else:
            st.error("Username or KEY error.")
    with st.expander("How to get an account and KEY"):
        st.write("You can ask :blue[Jeremy] for one(works only in the ramp), or get a *****test account*****. Test account is limited, so getting a real account is recommended.")
        with st.popover("Get a test account"):
            users = st.secrets.get("users", {})
            st.markdown(":red[Warning: ] Your test account is not private. Please protect your data.")
            if st.button("Get test account"):
                st.toast(f"""Your account is:  
***tester***  
Your KEY is :     
 ***{users['tester']['KEY']}***""",
                     icon="🔑")

# 注销函数
def logout():
    st.session_state.user = None
    st.session_state.role = None
    st.rerun()

# 模拟定义页面函数
def define_pages():
    # 这里简单返回空列表，实际应根据需求定义页面
    return [], [], [], [], []

# 模拟获取页面字典函数
def get_page_dict(account_pages, request_pages, test_pages, admin_pages, requestd_pages):
    return {}

# 主函数
def main():
    st.title(":rainbow[Ramp Website]")
    account_pages, request_pages, test_pages, admin_pages, requestd_pages = define_pages()
    page_dict = get_page_dict(account_pages, request_pages, test_pages, admin_pages, requestd_pages)

    if st.session_state.user:
        # 模拟导航操作，这里假设 st.navigation 是自定义导航函数
        st.write("You are logged in. Here is the main page.")
        if st.button("Log Out"):
            logout()
    else:
        login()

    if st.session_state.user and st.session_state.role != "Tester":
        with st.sidebar:
            messages = st.container(height=300)
            if prompt := st.chat_input("Message JereChat..."):
                messages.chat_message("user").write(prompt)
                messages.chat_message("jerechat", avatar="icon_small.png").write(f"Echo: {prompt}")
    elif st.session_state.user and st.session_state.role == "Tester":
        with st.sidebar:
            messages = st.container(height=300)
            if prompt := st.chat_input("Not Availible"):
                messages.chat_message("jerechat", avatar="icon_small.png").info(f"Sorry. JereChat assistant is not availible for test users.")

if __name__ == "__main__":
    main()