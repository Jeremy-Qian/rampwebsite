import sqlite3
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.logic import MathematicalEvaluation, TimeLogicAdapter, BestMatch, LogicAdapter
import re
from chatterbot.conversation import Statement
import time
import data_generator
import json
import os

# 自定义 TimeLogicAdapter，限制触发条件
class CustomTimeLogicAdapter(TimeLogicAdapter):
    def can_process(self, statement):
        time_keywords = ['what is the time', '几点', '什么时候']
        text = statement.text.lower()
        return any(keyword in text for keyword in time_keywords)


# 自定义数学适配器，处理无空格的数学表达式
class CustomMathAdapter(MathematicalEvaluation):
    def can_process(self, statement):
        pattern = r'(\d+[+\-*/]\d+)'
        return bool(re.search(pattern, statement.text))

    def process(self, input_statement, additional_response_selection_parameters):
        text = input_statement.text
        pattern = r'(\d+)([+\-*/])(\d+)'
        new_text = re.sub(pattern, r'\1 \2 \3', text)
        new_statement = Statement(text=new_text)
        return super().process(new_statement, additional_response_selection_parameters)



learn = False
learn_2 = True
# 创建一个名为 JereChat 的聊天机器人实例
chatbot = ChatBot(
    "JereChat",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            "import_path": "__main__.CustomMathAdapter",
            "priority": 2
        },
        {
            "import_path": "__main__.CustomTimeLogicAdapter",
            "priority": 1
        },
        {
            "import_path": "chatterbot.logic.BestMatch",
            "default_response": "I'm not sure how to answer that.",
            "maximum_similarity_threshold": 0.85,
            "priority": 3
        }
    ],
    database_uri='sqlite:///database.sqlite3',
    read_only=learn
)


def train_from_database(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT text, in_response_to FROM statements")
        rows = cursor.fetchall()
        conn.close()

        # 构建类似语料库的结构
        corpus = {
            "conversations": []
        }
        for text, in_response_to in rows:
            if in_response_to:
                corpus["conversations"].append([in_response_to, text])

        # 将语料库保存为临时文件
        temp_corpus_file = "./temp_corpus.json"
        with open(temp_corpus_file, "w", encoding="utf-8") as f:
            json.dump(corpus, f, ensure_ascii=False, indent=4)

        # 使用 ChatterBotCorpusTrainer 进行训练
        trainer = ChatterBotCorpusTrainer(chatbot)
        trainer.train(temp_corpus_file)

        # 删除临时文件
        if os.path.exists(temp_corpus_file):
            os.remove(temp_corpus_file)

        print("数据库数据训练完成！")
    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
    except Exception as e:
        print(f"发生其他错误: {e}")


# 简单的性能优化：缓存最近的回复
response_cache = {}


def get_response_with_cache(user_input):
    if user_input in response_cache:
        return response_cache[user_input]
    start_time = time.time()
    response = chatbot.get_response(user_input)
    # 如果 response 为 None，提供一个默认回复
    if response is None:
        response = Statement(text="Sorry. I don't understand you.")
        response.confidence = 0.2
    end_time = time.time()
    print(f"响应时间: {end_time - start_time:.4f} 秒")
    response_cache[user_input] = response
    return response


# 评估和反馈机制
def collect_feedback(user_input, response, db_path):
    feedback = input(f"你对回复 '{response}' 是否满意？(y/n/w): ")
    if feedback.lower() == 'n':
        correct_response = input("请提供正确的回复: ")
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            # 插入新的回复和对应的问题
            cursor.execute("INSERT INTO statements (text, in_response_to) VALUES (?, ?)", (correct_response, user_input))
            conn.commit()
            conn.close()
            print(f"已将正确回复保存到语料库: {correct_response}")
        except sqlite3.Error as e:
            print(f"保存到语料库时发生数据库错误: {e}")
    elif feedback.lower() == 'w':
        topic = input("请提供Topic: ")
        try:
            response = data_generator.add_wikipedia_info_to_corpus(topic,db_path="corpus.db")
        except Exception as e:
            print(f"保存到语料库时发生数据库错误: {e}")


if __name__ == "__main__":
    db_path = 'corpus.db'
    train_from_database(db_path)

    print("JereChat 已准备好，请开始与它聊天！")
    while True:
        try:
            user_input = input("你: ")
            if user_input.lower() == 'exit':
                break
            response = get_response_with_cache(user_input)
            print("JereChat: ", response)
            if learn_2:
                collect_feedback(user_input, response, db_path)
        except (KeyboardInterrupt, EOFError, SystemExit):
            break