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
        <!--
        <a href="https://contactus.streamlit.app">
            <li>Contact Us</li>
        </a>
        <a href="https://rampions.streamlit.app">
            <li>Old Ramp Website</li>
        </a>
        <a href="https://ramper.streamlit.app">
            <li>Back to Login</li>
        </a>
        -->
        <p>
        Sorry. No links available.
        </p>
        <a href=#footer>
            <li>See why</li>
        </a>
    </div>
    <div id="content2">
        <h1>The stories</h1>
        /* "see morre" expander(april fool's trick, see more>see more>) */
        <p>
            <details>
                <summary>See More</summary>
                <p>
                    <details>
                        <summary>See More</summary>
                        <p>
                            <details>
                                <summary>See More</summary>
                                <p>
                                    <details>
                                        <summary>See More</summary>
                                        <p>
                                            <details>
                                                <summary>See More</summary>
                                                <p>
                                                    <a href="#footer">
                                                        <summary>See More</summary>
                                                    </a>
                                                </p>
                                            </details>
                                        </p>
                                    </details>
                                </p>
                            </details>
                        </p>
                    </details>
                </p>
            </details>
    </div>
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
    text-align: center;
}}
#banner {{
    margin-bottom: 5px;
    padding: 0px;
    background-color: #a2d9ff;
    border: 1px solid black;
    text-align: left;
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
    clear: both;
    width: 25%;
    height: 300px;
    border: 1px solid black;
    text-align: left;
    padding: 10px;
    box-sizing: border-box; /* 确保内边距包含在元素的宽度和高度内 */
}}
#content2 {{
    clear: both;
    width: 100%;
    height: 300px;
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
    background-color: #a2d9ff;
}}
</style>
"""
st.html(html_code)