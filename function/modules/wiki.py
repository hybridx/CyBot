import json
import requests
import nltk
from nltk.corpus import stopwords
import re

stop_words = stopwords.words('english')
words = ["wiki", "mean"]

def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext

def getMeaning(word):
	language_code = "en-us"
	words = ""
	for w in word:
		words += w
	url = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&exintro=&titles=" + words.lower()
	r = requests.get(url)
	t = r.json()
	p = t["query"]["pages"]
	for i in p:
		o = i
		break
	return cleanhtml(t["query"]["pages"][o]["extract"])

def handle(text, ai):
	tokenized_words = nltk.word_tokenize(text)
	w = [word for word in tokenized_words if word not in stop_words + words]
	m = getMeaning(w)
	print(m)
	ai.text = "According to wikipedia "+m

def isValid(text):
	keymatch = 0;
	for w in words:
		for t in text:
			if t == w:
				keymatch = keymatch + 1
	return keymatch