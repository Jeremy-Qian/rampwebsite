import streamlit as st
import base64

st.set_page_config(
    page_title="Streamlit App",
    page_icon=":smile:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get help': 'https://contactus.streamlit.app',
        'Report a bug': "https://github.com/Jeremy-Qian/rampwebsite/issues",
        'About': "Streamlit App"
    }
)

file_ = open("banner_trick.png", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

# html code
html_code = f"""
<div id="container">
    <div id="banner">
        <a href="#footer">
            <img src="data:image/gif;base64,{data_url}" alt="Error showing banner(banner.gif). If you believe that this is an error, please contact us." style="width:100%; height:100%; object-fit: cover;"/>
        </a>
    </div>
    <div id="content">
        <h1>Danger! Danger!</h1>
        <p>
            Aliens have landed 2 miles north of the ramp, and are on its way to attack Shanghai South  
            Station on the first day of April.
        </p>
        <a href="#footer">
            <li>See More</li>
        </a>
        <br>
        <br>
    </div>
    <div id="links">
        <p>
            <h1>Links</h1>
        </p>
        <p>
            Sorry. No links available.
        </p>
        <a href="#footer">
            <li>See why</li>
        </a>
    </div>
    <div style="clear: both;"></div> <!-- 清除浮动 -->
    <div id="superlongscroll"></div>
    <div id="footer">April Fool! Scroll up... Forever!</div>
</div>
<style>
body {{
    width: 100%;
    margin: 10px;
}}
#container {{
    width: 100%;
    padding: 10px;
    box-sizing: border-box; /* 确保内边距包含在元素的宽度和高度内 */
}}
#banner {{
    margin-bottom: 5px;
    padding: 0px;
    background-color: #a2d9ff;
    border: 1px solid black;
    text-align: center;
}}
#content {{
    float: left;
    width: 75%;
    height: 300px;
    border: 1px solid black;
    text-align: left;
    padding: 10px;
    box-sizing: border-box; /* 确保内边距包含在元素的宽度和高度内 */
}}
#links {{
    float: right;
    width: 20%;
    height: 300px;
    padding: 10px;
    border: 1px solid black !important; /* 确保边框样式生效 */
    text-align: center;
    box-sizing: border-box; /* 确保内边距包含在元素的宽度和高度内 */
    margin: 10px; /* 添加 margin */
}}
#superlongscroll {{
    clear: both;
    width: 100%;
    height: 100000px;
}}
#footer {{
    clear: both;
    padding: 10px;
    border: 1px solid black;
    text-align: center;
}}
</style>
"""
st.html(html_code)