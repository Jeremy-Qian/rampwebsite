import streamlit as st   
import time  
import numpy as np
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string # to process standard python string
import os
import re

# 构建 corpus.txt 的完整路径
script_dir = os.path.dirname(os.path.abspath(__file__))
corpus_path = os.path.join(script_dir, 'corpus.txt')

# 使用完整路径打开文件
f = open(corpus_path, 'r', errors='ignore')
raw=f.read()
raw=raw.lower()# converts to lowercase

# 替代 nltk 的句子和单词分词
def split_into_sentences(text):
    return re.split('[.!?]', text)

def split_into_words(text):
    pattern = re.compile(r'[^a-zA-Z0-9\s]')
    cleaned_text = pattern.sub('', text.lower())
    return cleaned_text.split()

sent_tokens = split_into_sentences(raw)
word_tokens = split_into_words(raw)

# 简单的词形还原函数
def simple_lemmatize(word):
    if word.endswith('s'):
        return word[:-1]
    return word

# 替代 nltk 的词形还原
def LemTokens(tokens):
    return [simple_lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

# 替代 nltk 的归一化
def LemNormalize(text):
    pattern = re.compile(r'[^a-zA-Z0-9\s]')
    cleaned_text = pattern.sub('', text.lower())
    tokens = cleaned_text.split()
    return [simple_lemmatize(token) for token in tokens]

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def response(user_response):
    robo_response = ''
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if req_tfidf == 0:
        robo_response = "I am sorry! I don't understand you"
        return robo_response
    else:
        full_response = sent_tokens[idx]
        # 替代 nltk 的句子分割
        response_sentences = split_into_sentences(full_response)
        if len(response_sentences) > 3:
            robo_response = ' '.join(response_sentences[:3]) + "... [message truncated]"
        else:
            robo_response = full_response
        return robo_response

def generate_response(user_input):
    global word_tokens
    user_response = user_input.lower()
    if greeting(user_response) is not None:
        return greeting(user_response)
    else:
        sent_tokens.append(user_response)
        word_tokens = word_tokens + split_into_words(user_response)
        return response(user_response)

if "messages" not in st.session_state:  
    st.session_state.messages = []  

for msg in st.session_state.messages:  
    if msg["role"] == "bot":
        with st.chat_message(msg["role"], avatar="icon_small.png"):
            st.write(msg["content"])
    else:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])


prompt = st.chat_input("Say something...")  

if prompt:  
    st.session_state.messages.append({"role": "user", "content": prompt})  
    with st.chat_message("user"):  
        st.write(prompt)  
    first_time = time.time()
    bot_response = generate_response(prompt)
    second_time = time.time()
    elapsed_time = second_time - first_time
    elapse_text = f":gray-badge[Thought for {elapsed_time:.2f} seconds]  \n"
    st.session_state.messages.append({"role": "bot", "content": elapse_text + bot_response})  
    with st.chat_message("bot", avatar="icon_small.png"): 
        st.write(elapse_text + bot_response)