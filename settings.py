#settings.py
import streamlit as st
from streamlit_card import card 
st.header("Your Account")
st.write(f"Hello, {st.session_state.user}!")
def logout():
    st.session_state.user = None
    st.session_state.role = None
    st.rerun()
with st.popover("Stuff about my account"):
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
        try:
            a = users[st.session_state.user]['KEY']
            del a
        except:
            st.markdown(":red[Sorry. You don't have a key.]")
        else:
            if st.button("Click to reveal", type="tertiary"):
                try:
                    st.toast(f"""Your KEY is :     
         ***{users[st.session_state.user]['KEY']}***""",
                             icon="🔑")
                except KeyError:
                    st.toast("Sorry. :red[You don't have a key.] \
    Maybe it's because you logged in using the Fast Login method.")
    if st.button("Log Out"):
        logout()

card(
    title="Log Out",
    text="Log out of your account",
)