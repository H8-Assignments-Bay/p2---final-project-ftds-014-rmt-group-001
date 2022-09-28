import streamlit as st
import requests
# Data structure
import json
from pandas import json_normalize
import numpy as np
import pandas as pd
# preprocessing
import re
from tensorflow import keras
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

    st.subheader("GuruBot")
    new_data = st.text_input('Ask Here')

    # Cleaning

    def clean(text):
        text = text.lower() # Lowering the case
        text = re.sub("[^A-Za-z\s']"," ", text) # Choosing only words
        return text

    new_data = clean(new_data)

    result = keras.preprocessing.sequence.pad_sequences(
        tokenizer.texts_to_sequences([new_data]),
        truncating='post', 
        maxlen=20)
    new_data_list = result

    input_data_json = json.dumps({
        "signature_name": "serving_default",
        "instances": new_data_list.tolist()
    })

    URL = "https://backend-stockguru-app-1.herokuapp.com/v1/models/chat_model:predict"
    r = requests.post(URL, data=input_data_json)
    res = r.json()

    ha = pd.DataFrame(res)
    ha1 = ha['predictions'].to_list()
    res = np.argmax(ha1)

    tag = lbl_encoder.inverse_transform([res])

    for i in data['intents']:
        if i['tag'] == tag:
            st.write(np.random.choice(i['responses']))