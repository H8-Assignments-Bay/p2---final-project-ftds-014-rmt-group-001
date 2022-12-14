from array import array
from os import sep
from tkinter.ttk import Separator
import streamlit as st
import requests
# Data structure
import json
from pandas import json_normalize
import numpy as np
import pandas as pd
# preprocessing
import re
import string
import html
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer

from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
import random
import pickle

def app():
    # Input Intents
    with open("intents.json") as file:
        data = json.load(file)

    # load tokenizer object
    with open('model/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open('model/label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    st.subheader("StockGuruu Chatbot")
    new_data = st.text_input('Ask Here')

    data1 = {'col':[new_data]}
    new_data = pd.DataFrame(data1)

    # Cleaning

    stemmer=SnowballStemmer(language = 'english')
    def clean(text):
        text = re.sub("[^A-Za-z\s']"," ", str(text)) # Choosing only words
        text = word_tokenize(text)
        text = [stemmer.stem(word) for word in text if word not in set(stopwords.words("english"))]
        text = " ".join(text)
        return text

    new_data['clean'] = new_data['col'].apply(clean)
    new_data = np.array(new_data['clean'])

    txt_seq = tokenizer.texts_to_sequences(new_data)

    result = keras.preprocessing.sequence.pad_sequences(
        txt_seq,
        truncating='post', 
        maxlen=20)

    # new sample data with list format

    new_data_list = result

    input_data_json = json.dumps({
        "signature_name": "serving_default",
        "instances": new_data_list.tolist()
    })

    URL = "https://backend-trial-sg.herokuapp.com/v1/models/chat_model:predict"
    r = requests.post(URL, data=input_data_json)
    res = r.json()

    ha = pd.DataFrame(res)
    ha1 = ha['predictions'].to_list()
    res = np.argmax(ha1)

    tag = lbl_encoder.inverse_transform([res])

    for i in data['intents']:
        if i['tag'] == tag:
            st.write(np.random.choice(i['responses']))
