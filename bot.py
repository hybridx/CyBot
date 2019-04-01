import telebot
import time
import nltk
import random
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

cybot = ChatBot('cybot')
cybot.set_trainer(ListTrainer)

# for file in os.listdir('english/'):
# 	data = open('english/'+file,'r').readlines()
# 	cybot.train(data)
# for file in os.listdir('hindi/'):
# 	data = open('hindi/'+file,'r').readlines()
# 	cybot.train(data)
# for file in os.listdir('marathi/'):
# 	data = open('marathi/'+file,'r').readlines()
# 	cybot.train(data)

def respnd(message):
			return cybot.get_response(message)

while True:
	try:
		BOT_URL = 'href="https://api.telegram.org/bot855637405:AAHUT9lZnm1fNbae6qNF2_zHMAnJJUbjsko/'

		bot_token = "855637405:AAHUT9lZnm1fNbae6qNF2_zHMAnJJUbjsko"

		bot = telebot.TeleBot(token=bot_token)

		@bot.message_handler(commands=['start'])
		def send_welcome(message):
		    bot.reply_to(message,'Welcome!')

		@bot.message_handler(commands=["help"])
		def send_help(message):
		    bot.reply_to(message,"To use the bot, send it ddk@<your search string> NOTE:the bot will search for the entire string after the search keyword. Why you ask? Beacuse its designed that way you DUM DUM!")

		@bot.message_handler(func=lambda m: m.text is not None and 'ddk@' in m.text.lower())
		def search_duckduckgo(message):
		    texts = message.text.lower().rsplit("ddk@")

		    if len(texts) > 1: searchString = texts[1].strip()
		    else: searchString = texts[0].strip()

		    bot.reply_to(message,"https://duckduckgo.com/?q="+"+".join(searchString.split()))

		@bot.message_handler(func=lambda m:True)
		def random_replies(message):
		    print(message.text)
		    bot.reply_to(message,respnd(message.text))

		i = 0
		while True:
		    try:
		        i += 1
		        print("Running . . . ",i,"times")
		        bot.polling()
		    except Exception:
		        time.sleep(30)
	except Exception as e:
		print("Exception:",e)