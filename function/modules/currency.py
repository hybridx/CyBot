import nltk
import requests
import json
from nltk.corpus import stopwords

stop_words = stopwords.words('english')

words = ["currency"]

def handle(text, ai):
	tokenized_words = nltk.word_tokenize(text)
	w = [word for word in tokenized_words if word not in stop_words + words]
	cur = w[0]
	url = "https://free.currconv.com/api/v7/convert?q="+cur+"&compact=ultra&apiKey=6d5c7cac201b98da22bc"
	r = requests.get(url)
	t = json.loads(r.text)
	ai.text = "A unit of "+cur.split('_')[0]+" is "+'%.2f'%t[cur]+" "+cur.split('_')[1]+" and a unit of "+cur.split('_')[1]+" is "+'%.2f'%(1/t[cur])+" "+cur.split('_')[0]

def isValid(text):
	keymatch = 0;
	for w in words:
		for t in text:
			if t == w:
				keymatch = keymatch + 1
	return keymatch