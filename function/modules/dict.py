import json
import requests
import nltk
from nltk.corpus import stopwords

stop_words = stopwords.words('english')
words = ["meaning", "mean"]

def lem(word):
	app_id  = "a1ab1230"
	app_key  = "f0864a82bc2e3b41d3458b1f26c92e32"
	endpoint = "lemmas"
	language_code = "en-us"
	word_id = "flabbergasted"
	url = "https://od-api.oxforddictionaries.com/api/v2/" + endpoint + "/" + language_code + "/" + word_id.lower()
	r = requests.get(url, headers = {"app_id": app_id, "app_key": app_key})
	t = r.json()
	return t["results"][0]["lexicalEntries"][0]["inflectionOf"][0]["text"]

def getMeaning(word):
	app_id  = "a1ab1230"
	app_key  = "f0864a82bc2e3b41d3458b1f26c92e32"
	endpoint = "entries"
	language_code = "en-us"
	word = word[0]
	word = lem(word)
	url = "https://od-api.oxforddictionaries.com/api/v2/" + endpoint + "/" + language_code + "/" + word.lower()
	r = requests.get(url, headers = {"app_id": app_id, "app_key": app_key})
	t = r.json()
	return t["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0]

def handle(text, ai):
	tokenized_words = nltk.word_tokenize(text)
	w = [word for word in tokenized_words if word not in stop_words + words]
	m = getMeaning(w)
	ai.text = "As per my dictionary says "+w[0]+" means "+m

def isValid(text):
	keymatch = 0;
	for w in words:
		for t in text:
			if t == w:
				keymatch = keymatch + 1
	return keymatch