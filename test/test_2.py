import streamlit as st

st.warning("This page is deprecated. It will be removed in the future.")

st.markdown("""
# Welcome to the calculator!
""")
# 定义计算器函数
def calculate(expression):
    """
    This function evaluates the given mathematical expression and returns the result.
    Parameters:
    - expression (str): The mathematical expression to be evaluated.
    Returns:
    - float: The result of the evaluated expression.
    """
    try:
        result = eval(expression)
        return result
    except Exception as e:
        st.error(f"Error: {e}")
        st.stop()   
        
# 获取用户输入
expression = st.text_input("Enter an expression:")
# 计算结果并显示
if st.button("Calculate"):
    if not expression:
        st.warning("Please enter an expression.")
        st.stop()
    result = calculate(expression)
    st.write("Result:", result)