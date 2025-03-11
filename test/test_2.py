import streamlit as st
from streamlit_extras import add_vertical_space as avs
from streamlit_extras.grid import grid

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

# 使用 streamlit_extras 的 grid 组件创建网格布局
my_grid = grid(5, 4, vertical_align="center")

# 显示输入框
with my_grid.container():
    st.text_input("输入/结果", st.session_state.input, disabled=True, key="display")

# 添加按钮
for row in buttons:
    for button in row:
        if button == "=":
            # 单独处理 "=" 按钮，跨越多列
            if my_grid.button(button, use_container_width=True):
                try:
                    # 计算表达式的结果
                    st.session_state.input = str(eval(st.session_state.input))
                except Exception as e:
                    st.session_state.input = "错误"
        elif button == "C":
            if my_grid.button(button, use_container_width=True):
                # 清空输入
                st.session_state.input = ""
        else:
            if my_grid.button(button, use_container_width=True):
                # 追加按钮值到输入
                st.session_state.input += button