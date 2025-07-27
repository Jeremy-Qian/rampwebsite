import streamlit as st
st.write("## Download our apps")
st.warning("Warning: This is only a test app. It will cost you 15MB of space and will do nothing.")
with open('root.dmg','rb') as file:
    st.download_button(
        label="Download the 'Root' app",
        data=file,
        file_name="root.dmg",
        mime="application/x-apple-diskimage",
        icon=":material/download:",
    )
st.write("After downloading, open the DMG file and drag root.app to the Applications folder. This is what it looks like:")
st.image("images/root_app_demo.png")