import streamlit as st
import base64

st.set_page_config(
    page_title="Home",
    page_icon=":material/home:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get help': 'https://contactus.streamlit.app',
        'Report a bug': "https://github.com/Jeremy-Qian/rampwebsite/issues",
        'About': "Streamlit App"
    }
)

st.markdown(":red-badge[A big problem] This page has a BIG problem. Wait for a few days/weeks...")