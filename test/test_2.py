import streamlit as st

# 设置页面标题
st.title("网格按钮计算器")

# 初始化 session_state 用于存储输入和结果
if "input" not in st.session_state:
    st.session_state.input = ""

# 定义按钮的布局
buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "C", "+"],
    ["="]
]

# 显示输入框
st.text_input("输入/结果", st.session_state.input, disabled=True, key="display")

# 使用 st.columns 创建网格布局
for row in buttons:
    cols = st.columns(len(row))  # 根据每行的按钮数量创建列
    for i, button in enumerate(row):
        if cols[i].button(button, use_container_width=True):
            if button == "=":
                try:
                    # 计算表达式的结果
                    st.session_state.input = str(eval(st.session_state.input))
                except Exception as e:
                    st.session_state.input = "错误"
            elif button == "C":
                # 清空输入
                st.session_state.input = ""
            else:
                # 追加按钮值到输入
                st.session_state.input += button

    # 添加垂直间距（可选）
    st.write("")  # 空行用于分隔按钮行