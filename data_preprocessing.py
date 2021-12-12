import string
import pandas as pd

def preprocess(text):
    # convert to lower case
    text = text.lower()
    # remove punctuation
    tr_table = str.maketrans({key: None for key in string.punctuation})
    text = text.translate(tr_table)
    return text

# load the jokes data
jokes = pd.read_csv("data/dad_jokes.csv")
# load the evil insults data
insults = pd.read_csv("data/insults.csv")

# drop the id column and add the class column
# class 0 - Joke, 1 - Insult
jokes = jokes.drop('Id', axis=1)
jokes['class'] = 0
insults = insults.drop('Id', axis=1)
insults['class'] = 1

# rename columns and create a combined dataset
jokes.rename(columns={"Joke": "doc"}, inplace=True)
insults.rename(columns={"Insult": "doc"}, inplace=True)
# concat
df = pd.concat([jokes, insults])

# apply the text preprocessing on the dataset
df['doc'] = df['doc'].apply(lambda x: preprocess(x))

# save the dataset for later use
df.to_csv("data/data.csv", index=False)


