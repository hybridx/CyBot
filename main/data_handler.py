import json
import pymongo
import logging
import os

import time
import random


def get_random_num():
	return str(random.randint(1, 987654321) + sum(map(int,str(time.time()).split("."))))



logging.basicConfig(filename='../logs/app.log', 
	filemode='w+', 
	format='%(name)s - %(levelname)s - %(message)s')

logging.basicConfig(level=logging.DEBUG)

template = {
    "rasa_nlu_data": 
    {
        "common_examples": [],
        "regex_features" : [],
        "lookup_tables"  : [],
        "entity_synonyms": []
    }
}
try:
	mongodb = pymongo.MongoClient(username="admin",password="root",authSource="admin")
	master = mongodb.master
except Exception as e:
	exptns(e,info)

'''
Log levels
logging.DEBUG  		->		10
logging.INFO  		->		20
logging.WARNING  	->		30
logging.ERROR  		->		40
logging.CRITICAL  	->		50
'''
debug = logging.DEBUG
info = logging.INFO
warning = logging.WARNING
error = logging.ERROR
critical = logging.CRITICAL

def exptns(e,level=debug):
	logging.basicConfig(level=level)
	logging.debug('Exception --> This is a debug message -> {}'.format(e))
	logging.info('Exception --> This is an info message -> {}'.format(e))
	logging.warning('Exception --> This is a warning message -> {}'.format(e))
	logging.error('Exception --> This is an error message -> {}'.format(e))
	logging.critical('Exception --> This is a critical message -> {}'.format(e))


try:
	mongodb = pymongo.MongoClient(username="admin",password="root",authSource="admin")
except Exception as e:
	exptns(e,warning)


def load_file_data(username="original"):
	'''
	Returns data set in json format if available else e
	'''
	try:
		with open("./data/{}-custom.json".format(username),"r+") as fp:
			return json.load(fp)
	except Exception as e:
		exptns(e,error)
		return e

def save_file_data(username="original",data=template):
	'''
	Returns True if the data is save else e
	'''
	try:
		with open("./data/{}-custom.json".format(username),"w") as fp:
			json.dump(data, fp)
			return True
	except Exception as e:
		exptns(e,info)
		return e


def save_data_mongo(username="original",data=template):
	collection = get_collection_from_db(username)
	'''
	Returns True if data inserted else e
	'''
	'''
	if type(answers) == type(list()):
		answers_data = {"intent":intent,"conversation":answers}
	else:
		answers_data = {"intent":intent,"conversation":[answers]}
	'''
	try:
		if collection.find({"intent":data["intent"]}).count() > 0:
			if type(data["conversation"]) == type(list()):
				for i in data["conversation"]:
					collection.update({"intent":data["intent"]},{'$push':{'conversation':i}})
			else:
				collection.update({"intent":data["intent"]},{'$push':{'conversation':data["conversation"]}})
		else:
			if type(data["conversation"]) == type(list()):
				collection.insert({"intent":data["intent"],"conversation":data["conversation"]})
			else:
				collection.insert({"intent":data["intent"],"conversation":[data["conversation"]]})
		return True
	except Exception as e:
		exptns(e,info)
		return e

def remove_data_mongo(username="original",intent='greet'):
	'''
	Returns removed element
	'''
	try:
		if "{}".format(username) in master.list_collection_names():
			collection = master.get_collection("{}".format(username))
		else:
			collection = master.create_collection(username)

		response = collection.find_one_and_delete({"intent":intent})
		return response
	except Exception as e:
		exptns(e,info)
		return e


def update_mongo_data(username='original',intent='greet',answers="default"):
	try:
		collection = get_collection_from_db(username)

		if collection.count_documents({"intent":intent}) > 0:
			collection.insert({"intent":intent,'conversation':data})

		if type(answers) == type(list()):
			collection.update({"intent":intent}, {'$set':{'conversation':data}})
		else:
			collection.update({"intent":intent}, {'$set':{'conversation':[data]}})
	except Exception as e:
		exptns(e,info)
		return e


def get_mongo_response(username="original",intent="default"):
	'''
	Returns the response for a respective user
	'''
	collection = get_collection_from_db(username)


	if collection.count_documents({"intent":intent}) > 0:
		response = collection.find({"intent":intent})[0]["conversation"]
		return response
	else:
		collection = master.original
		if collection.count_documents({"intent":intent}) > 0:
			response = collection.find({"intent":intent})[0]["conversation"]
			return response
		else:
			return collection.find({"intent":"default"})[0]["conversation"]


def get_all_intents(username="original"):
	collection = get_collection_from_db(username)

	data = []
	
	if collection.find().count() > 0:
		for i in collection.find():
			data.append(i["intent"])
		return {"count":collection.find().count(),"intents":data}
	else:
		return {"count":collection.find().count(),"intents":None}


def get_intent_data(username="original",intent="default"):
	collection = get_collection_from_db(username)

	questions = load_file_data(username = username)
	questions = [i["text"] for i in questions["rasa_nlu_data"]["common_examples"] if i["intent"] == intent]

	answers = collection.find({"intent":intent})[0]["conversation"]

	return {"intent":intent,"answers":answers,"questions":questions}

def save_conversation(username="original",user_text="default",bot_text="default"):
	return None



def check_file_exists(username="original"):
	return os.path.isfile("./data/{}-custom.json".format(username))






def get_collection_from_db(username = "original"):
	if "{}".format(username) in master.list_collection_names():
		collection = master.get_collection("{}".format(username))
	else:
		collection = master.create_collection(username)

	return collection