import streamlit as st
hide_github_icon = """
#GithubIcon {
  visibility: hidden;
}
"""
st.markdown(hide_github_icon, unsafe_allow_html=True)
try:
    # 从secrets中获取正确的code
    correct_code = st.secrets["code"]
    #st.session_state['logged_in'] = False
    @st.dialog("Log In as Ramper")
    def login():
        with st.expander("Help"):
            st.write("""
            > Ramp Website  
            > Created on July 24, 2024 by Jeremy Qian  
            > To view the website, you have to be a rampion.  
            -------------------------------------
            Please enter the code shown in the [Ramp Group](https://chat.google.com) to log in.  
            Don't worry if you see a red 'KeyError' message under this dialog, once you log in it will dissapear.  
            The code is not case sensitive. You could enter it in upper or lower case.
            #### :red[WARNING:]
            Don't press the "X" button. If you do, you will fall into the error message and will have to rerun.""")
        # 创建密码输入框
        user_input_code = st.text_input("Enter the code shown in the [Ramp Group](https://chat.google.com)", type="password")
        # 验证用户输入的code是否正确
        if st.button("Log In"):
            if user_input_code.upper() == correct_code:
                st.success("Correct! Now press the x button.")
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Password Error. Please try again.")
    if 'logged_in' not in st.session_state :
        login()

    if st.session_state['logged_in']:
        st.title(":rainbow[Ramp Website]")
        pages = {
        "Home":[
            st.Page("home/ads.py", title="Ads"),
        ],
        "Rampion's Fast Fun": [
            st.Page("fun/jerechat.py", title="JereChat 1 Pro", icon=":material/robot:"),
            st.Page("fun/news.py", title="News"),
        ],
        }

        pg = st.navigation(pages)
        pg.run()
except KeyError:
    pass