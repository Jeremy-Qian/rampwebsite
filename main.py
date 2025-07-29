import streamlit as st
import random as rm
@st.dialog(title="The Girl's Club")
def girlsclubad():
    st.markdown(":gray[AD]", help="This is an ad, and the Girl's Club is sponsored. Learn more [here](rampion.streamlit.app).")
    st.image("images/girlsclub.jpeg")
    st.write("Join the ramp Girl's Club NOW! If you are a girl, of course.")

pages = {
    "Home": [
        st.Page("home.py", title="Home", icon=":material/home:",default=True),
    ],
    "Resources": [
        st.Page("resources/download.py", title="Download our apps", icon=":material/download:"),
        st.Page("resources/news.py", title="News", icon=":material/news:"),
        st.Page("resources/about.py", title="About", icon=":material/info:")
    ],
    "Ramp": [
        st.Page("polls.py", title="Polls and Debates", icon=":material/forum:")
    ],
}

st.title(":rainbow[The Ramp Website 2.0]")
pg = st.navigation(pages, position="top")
pg.run()
girlsclubad()
