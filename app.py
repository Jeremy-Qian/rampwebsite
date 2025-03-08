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

# 定义页面
def define_pages():
    logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
    settings = st.Page("settings.py", title="Settings", icon=":material/settings:")
    request_1 = st.Page(
        "request/request_1.py",
        title="Who's coming to the ramp?",
        icon=":material/help:",
    )
    request_2 = st.Page("request/request_2.py", title="Ramp Chat", icon=":material/chat:")
    test_1 = st.Page(
        "test/test_1.py",
        title="Welcome!",
        icon=":material/scooter:",
        default=True,
    )
    admin_1 = st.Page(
        "admin/admin_1.py",
        title="Admin 1",
        icon=":material/person_add:",
    )
    admin_2 = st.Page("admin/admin_2.py", title="Admin 2", icon=":material/security:")
    requestd_1 = st.Page(
        "disabled/dis_1.py",
        title="Who's coming to the ramp?",
        icon=":material/help:",
    )
    requestd_2 = st.Page("disabled/dis_2.py", title="Ramp Chat", icon=":material/chat:")
    account_pages = [logout_page, settings]
    request_pages = [request_1, request_2]
    requestd_pages = [requestd_1, requestd_2]
    test_pages = [test_1]
    admin_pages = [admin_1, admin_2]

    return account_pages, request_pages, test_pages, admin_pages, requestd_pages

# 权限控制
def get_page_dict(account_pages, request_pages, test_pages, admin_pages, requestd_pages):
    page_dict = {}
    if st.session_state.role in ["Requester", "Tester", "Admin"]:
        page_dict["Main Page"] = test_pages
    if st.session_state.role in ["Requester", "Admin"]:
        page_dict["Request"] = request_pages
    else:
        page_dict["Disabled"] = requestd_pages
    if st.session_state.role == "Admin":
        page_dict["Admin"] = admin_pages
    return page_dict

# 主函数
def main():
    st.title(":rainbow[Ramp Website]")
    account_pages, request_pages, test_pages, admin_pages, requestd_pages = define_pages()
    page_dict = get_page_dict(account_pages, request_pages, test_pages, admin_pages, requestd_pages)

    if st.session_state.user:
        pg = st.navigation({"Account": account_pages} | page_dict)
    else:
        pg = st.navigation([st.Page(login)])

    pg.run()
    with st.sidebar:
        messages = st.container(height=300)
        if prompt := st.chat_input("Say something"):
            messages.chat_message("user").write(prompt)
            messages.chat_message("assistant").write(f"Echo: {prompt}")

if __name__ == "__main__":
    main()