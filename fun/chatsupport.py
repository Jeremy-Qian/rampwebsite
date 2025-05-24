import nltk
import numpy as np
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string # to process standard python string
import os

# 构建 corpus.txt 的完整路径
script_dir = os.path.dirname(os.path.abspath(__file__))
corpus_path = os.path.join(script_dir, 'corpus.txt')

# 使用完整路径打开文件
f = open(corpus_path, 'r', errors='ignore')
raw=f.read()
raw=raw.lower()# converts to lowercase
nltk.download('punkt') # first-time use only
nltk.download('wordnet') # first-time use only
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words
lemmer = nltk.stem.WordNetLemmatizer()
#
def LemTokens(tokens):
   return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
   return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
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
        # Split the response into sentences
        response_sentences = nltk.sent_tokenize(full_response)
        
        # If there are multiple sentences, return just the first few
        if len(response_sentences) > 3:
            robo_response = ' '.join(response_sentences[:3]) + "... [message truncated]"
        else:
            robo_response = full_response
        
        return robo_response

def generate_response(user_input):
    user_response=user_response.lower()
    if(greeting(user_response)!=None):
        return greeting(user_response)
    else:
        sent_tokens.append(user_response)
        word_tokens=word_tokens+nltk.word_tokenize(user_response)
        return(response(user_response))
