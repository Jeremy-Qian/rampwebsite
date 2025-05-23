import streamlit as st

# 从secrets中获取正确的code
correct_code = st.secrets["code"]
st.session_state['logged_in'] = False
@st.dialog("Log In as Ramper")
def login():
    # 创建密码输入框
    user_input_code = st.text_input("Enter the code shown in the Ramp Group", type="password")

    # 验证用户输入的code
    if user_input_code == correct_code:
        st.success("Correct! Press the continue button and then press the x button.")
        st.session_state['logged_in'] = True
        if st.button("Continue"):
            st.rerun()
    else:
        st.error("Password Error. Please try again.")
if not st.session_state['logged_in']:
    login()

if st.session_state['logged_in']:
    st.title("Experimental Content")
    st.write("lalalalalal")
    st.write("blah")