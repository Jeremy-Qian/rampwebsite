import streamlit as st
import base64

st.set_page_config(
    page_title="Login",
    page_icon=":material/account_circle:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get help': 'https://contactus.streamlit.app',
        'Report a bug': "https://github.com/Jeremy-Qian/rampwebsite/issues",
        'About': "Streamlit App"
    }
)
@st.dialog("Fast Login")
def fast_login():
    st.markdown("#### :red[**Who invented the ramp game see you?**]")
    st.markdown("##### :gray[Examples:]  \n:green-badge[:material/check: John]:red-badge[:material/close: John Appleseed]:red-badge[:material/close: john]:red-badge[:material/close: john appleseed]")
    st.text_input("Enter your answer",key="fast_login")
    if st.button("Submit"):
        if st.session_state.fast_login == st.secrets.answer:
            st.success("Correct!")
            st.session_state.clear()
            st.link_button("Continue →",url="https://pleaseusethiswebsitedirectlywithoutlogginginyouarearamper.streamlit.app")
        else:
            st.error("Incorrect!")
            st.session_state.clear()
st.title(":rainbow[Ramp Website]")
st.markdown("##### **Fast Login :green-badge[:material/cake: New]**",help="The fast login is finally here!")
if st.button("Question: Click to reveal"):
    fast_login()