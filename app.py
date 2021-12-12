import random
import requests
import string
import pickle
import streamlit as st

# function to get a either a dad joke or an evil insult at random
def get_text():
    flag = True
    fails = 0
    while flag:
        try:
            k = random.choice([0, 1])
            if k == 0:
                response = requests.get('https://icanhazdadjoke.com/', headers={'Accept': 'application/json'})
                response = response.json()
                text = response['joke']
            else:
                response = requests.get('https://evilinsult.com/generate_insult.php?lang=en&type=json')
                response = response.json()
                text = response['insult']
            flag = False
        except:
            fails += 1
            if fails == 5:
                return None
            continue
    return text

# function to load the model
def load_model(model_name):
    with open(model_name, "rb") as file:
        model = pickle.load(file)
    return model

# function to preprocess the text
def preprocess(text):
    # convert to lower case
    text = text.lower()
    # remove punctuation
    tr_table = str.maketrans({key: None for key in string.punctuation})
    text = text.translate(tr_table)
    return text

# function to check whether the given text is joke or insult
def joke_or_insult(text, model):
    text = preprocess(text)
    X = [text]
    prediction = model.predict(X)[0]
    proba = model.predict_proba(X)[0]
    return (prediction, proba)


st.header("Is it a DAD JOKE or an EVIL INSULT???")
# laod the model
model = load_model("knn_model.pkl")

# get the text from api
if st.button("Generate Text!"):
    text = get_text()
    # display the text
    st.title(text.replace('\n', ' '))
    # preprocess the text 
    text = preprocess(text)
    # predict using the model
    pred, proba = joke_or_insult(text, model)
    # print the result
    class_map = {0: 'Joke', 1: 'Insult'}
    article_map = {0: 'a', 1: 'an'}
    result = "The above text is {} {} with probability {:.2f}%".format(article_map[pred], 
                                                                    class_map[pred], 
                                                                    proba[pred]*100)
    st.write(result)

