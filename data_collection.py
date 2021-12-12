import requests
import pandas as pd
import tqdm as tqdm

# get dad jokes from the dad jokes public api
joke_ids = []
jokes = []

for i in tqdm(range(300)):
    try:
        response = requests.get("https://icanhazdadjoke.com/",
                            headers={'Accept': 'application/json'})
        response = response.json()
        joke_ids.append(response['id'])
        jokes.append(response['joke'])
    except:
        break

# create dataframe of dad jokes
jokes = pd.DataFrame({
    'Id': joke_ids,
    'Joke': jokes
})
# remove duplicates
jokes_df = jokes.drop_duplicates()
# save data for later use
jokes_df.to_csv("data/dad_jokes.csv", index=False)


# get evil insults from the evil insults public api
# get insults
insult_ids = []
insults = []

for i in tqdm(range(300)):
    try:
        response = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json")
        response = response.json()
        insult_ids.append(response['number'])
        insults.append(response['insult'])
    except:
        break

# create dataframe of insults
insults_df = pd.DataFrame({
    'Id': insult_ids,
    'Insult': insults
})
# remove duplicates
insults_df = insults_df.drop_duplicates()
# save data for later use
insults_df.to_csv("data/insults.csv", index=False)
