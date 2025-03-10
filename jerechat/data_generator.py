import sqlite3
import wikipedia
import requests
import certifi


def add_wikipedia_info_to_corpus(topic, db_path='corpus.db'):
    try:
        # 设置语言为中文，可根据需要修改
        wikipedia.set_lang("en")

        # 创建一个 requests Session 并指定证书路径
        session = requests.Session()
        session.verify = certifi.where()

        # 使用猴子补丁替换 wikipedia 库内部的会话
        wikipedia.wikipedia.requests = session

        # 获取维基百科上关于该主题的摘要
        summary = wikipedia.summary(topic, sentences=2)

        # 连接到数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 插入信息到 statements 表
        cursor.execute("INSERT INTO statements (text, in_response_to) VALUES (?,?)", (summary, f"What is {topic}?"))
        conn.commit()
        conn.close()
        print(f"有关 {topic} 的内容已保存到语料库。")
    except wikipedia.exceptions.PageError:
        print(f"未找到关于 {topic} 的维基百科页面。")
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"找到多个关于 {topic} 的页面，请明确指定。可能的选项有: {e.options}")
    except sqlite3.Error as e:
        print(f"数据库错误: {e}")


if __name__ == "__main__":
    while True:
        topic = input(">>> ")
        if topic.lower() == 'exit':
            break
        add_wikipedia_info_to_corpus(topic)