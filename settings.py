#settings.py
import streamlit as st
from streamlit_card import card 
st.header("Settings Page")
st.write("This is the settings page.")
def logout():
    st.session_state.user = None
    st.session_state.role = None
    st.rerun()
with st.popover("My Account"):
    st.markdown("""
<style>
button {
    height: 8px;
    width: 20px;
}
</style>
""", unsafe_allow_html=True)
    users = st.secrets.get("users", {})
    st.write(f"Your username: {st.session_state.user}")
    st.write(f"Your role: {st.session_state.role}")
    col1,col2=st.columns(2)
    with col1:
        st.write(f"Your KEY:")
    with col2:
        if st.button("Click to reveal", type="tertiary"):
            st.toast(f"""Your KEY is :     
 ***{users[st.session_state.user]['KEY']}***""",
                     icon="🔑")
    if st.button("Log Out"):
        logout()
