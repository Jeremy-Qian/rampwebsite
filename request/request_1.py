import streamlit as st
import json
import os
from datetime import datetime
import time

DISCLAIMER = """# Disclaimer

This website provides a platform where users can indicate their intention to come to the ramp by clicking a button. However, the following points should be noted:

## 1. Intention Representation
- Clicking the button "I am" only represents the user's current intention to come to the ramp at the time of clicking. It does not guarantee that the user will actually arrive at the ramp. There may be various unforeseen circumstances such as sudden emergencies, changes in personal schedules, or transportation issues that prevent the user from fulfilling this intention.

## 2. No Legal Obligation
- The act of clicking the button does not create any legal obligation on the part of the user. The website does not assume that the user is bound by a contract or agreement simply by clicking the button. The user is not liable for any damages or losses that may occur to other parties if they fail to come to the ramp after clicking the button.

## 3. Accuracy of Information
- The information displayed on the website regarding who has clicked the button is based on the data collected at the time of button - clicking. We strive to ensure the accuracy of this data, but we cannot guarantee its absolute accuracy due to potential technical glitches, data transfer errors, or human - made mistakes. We are not responsible for any inaccuracies in the displayed information.

## 4. External Factors
- The website has no control over external factors that may affect a user's ability to come to the ramp. These factors may include, but are not limited to, natural disasters, public health emergencies, or changes in local regulations. In such cases, the user's inability to come to the ramp is not the responsibility of the website or its operators.

## 5. No Warranty
- The website is provided "as is" without any warranty, either express or implied. We do not warrant that the service will be uninterrupted, error - free, or that the information provided will be completely accurate or reliable.

By using this website and clicking the button "I am", you acknowledge and agree to the terms of this disclaimer."""
DISCLAIMER_CHINESE = """# 免责声明

本网站为用户提供了一个通过点击按钮来表明前往南站意向的平台。不过，还请留意以下几点：

## 1. 意向说明
- 点击"I am"按钮仅代表用户在点击瞬间有前往南站的当前意向。这并不意味着用户一定会实际到达南站。可能会出现各种不可预见的状况，比如突发紧急事件、个人日程安排变动或者交通受阻等，从而导致用户无法达成前往南站的意向。

## 2. 无法律责任
- 点击按钮这一行为不会让用户承担任何法律责任。本网站不会仅仅因为用户点击了"I am"按钮，就认定用户受某一合同或协议的约束。若用户在点击按钮后未能前往南站，对于由此可能给其他方造成的任何损害或损失，用户无需承担责任。

## 3. 信息准确性
- 网站上所展示的关于哪些用户点击了按钮的信息，是基于点击按钮那一刻所收集的数据。我们会尽最大努力确保这些数据的准确性，但由于可能存在技术故障、数据传输错误或人为失误等因素，无法保证其绝对准确无误。对于所显示信息中的任何不准确之处，我们概不负责。

## 4. 外部因素
- 本网站无法对可能影响用户前往南站的外部因素进行控制。这些因素包括但不限于自然灾害、公共卫生突发事件或当地法规的变更等。在这些情况下，用户未能前往南站并非本网站或其运营方的责任。

## 5. 无保证条款
- 本网站“按现状”提供服务，不提供任何明示或暗示的保证。我们不保证服务能够持续不间断、毫无差错，也不保证所提供的信息完全准确可靠。

使用本网站并点击"I am"按钮即表示您认可并同意本免责声明的各项条款。"""
col1, col2 = st.columns(2)
with col1:
    with st.expander("Disclaimer(English)"):
        st.write(DISCLAIMER)
with col2:
    with st.expander("免责声明（中文）"):
        st.write(DISCLAIMER_CHINESE)
# JSON文件路径
JSON_FILE = 'ramp_attendees.json'

# 从JSON文件读取数据并初始化会话状态
def load_data():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as f:
            try:
                data = json.load(f)
                return data
            except json.JSONDecodeError:
                return []
    return []

# 将数据保存到JSON文件
def save_data(data):
    with open(JSON_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# 初始化会话状态
if 'names' not in st.session_state:
    st.session_state.names = load_data()

# 显示标题
st.header("Who's Coming to the ramp?")
but_col_1, but_col_2 = st.columns(2)
with but_col_1:
    # 当用户点击按钮时，添加名字和报名时间到会话状态和JSON文件
    if st.button("I am!",type="primary",use_container_width=True):
        name = st.session_state.user
        # 获取当前日期
        today = datetime.now().strftime("%Y-%m-%d")
        for entry in st.session_state.names:
            if entry["name"] == name and entry["signup_date"] == today:
                st.warning("You already signed up today.")
                break
        else:
            # 获取当前日期和时间
            signup_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_entry = {"name": name, "signup_date": today, "signup_time": signup_time}
            st.session_state.names.append(new_entry)
            save_data(st.session_state.names)
            st.success(f"{name} is coming to the ramp! Signed up at {signup_time}")
with but_col_2:
    # 添加更新按钮
    if st.button("Update List",type="secondary",use_container_width=True):
        st.session_state.names = load_data()
        st.info("List updated!")

# 显示所有要来南站的人的名字和报名时间，并根据角色决定是否显示删除按钮
if st.session_state.names:
    st.subheader("People who's coming to the ramp: ")
    sorted_names = sorted(st.session_state.names, key=lambda x: x["signup_time"], reverse=True)
    for idx, entry in enumerate(sorted_names, start=1):
        col1, col2, col3 = st.columns([3, 3, 1])
        with col1:
            st.write(f"{idx}. {entry['name']}")
        with col2:
            st.write(f"Signup Time: {entry['signup_time']}")
        with col3:
            can_delete = False
            today = datetime.now().strftime("%Y-%m-%d")
            if st.session_state.role == "Admin":
                can_delete = True
            elif entry["name"] == st.session_state.user and entry["signup_date"] == today:
                can_delete = True

            if can_delete:
                if st.button(f"Delete {entry['name']}", key=f"delete_{entry['name']}{entry['signup_time']}"):
                    st.session_state.names.remove(entry)
                    save_data(st.session_state.names)
                    st.rerun()
else:
    st.info("Nobody has signed up yet.")