import streamlit as st
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot_math import MathAdapter

# 创建 ChatBot 实例并添加 MathAdapter
chatbot = ChatBot(
    "MathBot",
    logic_adapters=[
        {
            "import_path": "chatterbot_math.MathAdapter",  # 使用 MathAdapter
            "math_words": ["计算", "等于", "结果"],  # 自定义触发数学计算的词语
        },
        "chatterbot.logic.BestMatch",  # 添加其他适配器以支持更多功能
    ]
)

# 训练 ChatBot（可选）
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")  # 训练英文语料库

# 设置页面标题
st.title("聊天式计算器")

# 初始化 session_state 用于存储聊天记录
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 显示聊天记录
for message in st.session_state.chat_history:
    st.write(f"{message['role']}: {message['text']}")

# 用户输入
user_input = st.text_input("输入数学表达式（例如：2 + 2）", key="user_input")

# 处理用户输入
if st.button("发送"):
    if user_input:
        # 将用户输入添加到聊天记录
        st.session_state.chat_history.append({"role": "你", "text": user_input})

        # 获取 ChatBot 的回复
        response = chatbot.get_response(user_input)

        # 将 ChatBot 的回复添加到聊天记录
        st.session_state.chat_history.append({"role": "计算器", "text": response})

        # 清空输入框
        st.session_state.user_input = ""

# 重新渲染页面以显示更新后的聊天记录
st.experimental_rerun()