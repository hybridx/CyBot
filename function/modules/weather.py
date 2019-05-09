import nltk
import requests
import json
from nltk.corpus import stopwords

stop_words = stopwords.words('english')

words = ["weather"]


def handle(text, ai):
	tokenized_words = nltk.word_tokenize(text)
	w = [word for word in tokenized_words if word not in stop_words + words]
	# print(w)
	# url = 'https://dialogflow.googleapis.com/v2beta1/projects/cyrus-237322/agent/sessions/05786dc3-07d1-0f09-ce2a-12a4c7ca176e:detectIntent'
	# payload = "{\"queryInput\":{\"text\":{\"text\":\""+text+"\",\"languageCode\":\"en\"}},\"queryParams\":{\"timeZone\":\"Asia/Calcutta\"}}"
	# headers = {'Content-Type': 'application/json', 'charset': 'utf-8', 'Authorization': "Bearer ya29.c.EloBBwEpTOy1Dr90DS_zFdciF92dx5bJ50JawSwjwRLlwj6fTrg1zD7vWK7iW7Qw8sc06o6C2KPuIwRRM5FyVCD9u8WjE5uCaYUVGVqlOJ-wPMkl_gCxGVG-ByQ"}
	# r = requests.post(url, data=payload, headers=headers)
	# j = json.loads(r.text)
	# c = j["queryResult"]["parameters"]["geo-city"]
	# print(j["queryResult"]["parameters"]["geo-city"])
	# url = "http://api.openweathermap.org/data/2.5/weather?q="+c+"&APPID=5fdda0bf1e4f2581de5ac33be8fdd427"
	# r = requests.get(url)
	# j = json.loads(r.text)
	tx = '{"coord":{"lon":-73.99,"lat":40.73},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"base":"stations","main":{"temp":296.42,"pressure":1014,"humidity":38,"temp_min":293.71,"temp_max":298.71},"visibility":16093,"wind":{"speed":2.1},"clouds":{"all":1},"dt":1556039032,"sys":{"type":1,"id":5141,"message":0.0121,"country":"US","sunrise":1556013930,"sunset":1556062965},"id":5128581,"name":"New York","cod":200}'
	j = json.loads(tx)
	print(j)
	ai.text = "The weather in "+j["name"]+" seems to be "+j["weather"][0]["main"]+" with temperature "+str('%.2f'%(j["main"]["temp"]-273.15))+" Celcius"

def isValid(text):
	keymatch = 0
	for w in words:
		for t in text:
			if t == w:
				keymatch = keymatch + 1
	return keymatch