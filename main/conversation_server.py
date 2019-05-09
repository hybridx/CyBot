from flask import Flask, request, render_template, jsonify
from flask_cors import CORS, cross_origin
import json
from conversation_model import get_intent
import pymongo
import random
import requests
from data_handler import load_file_data, save_data_mongo, save_file_data, check_file_exists, remove_data_mongo, update_mongo_data, get_mongo_response, get_all_intents, get_intent_data

#Connection
#------------------

mongodb = pymongo.MongoClient(username="admin",password="root",authSource="admin")
conversations = mongodb.conversation.chatData

#------------------

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/get_response',methods=['POST'])
def index():
	text = str(request.get_data(),"utf-8")
	msg = json.loads(text)
	msg = msg["text"]
	msg = msg["username"]
	intent = json.loads(get_intent(msg))
	intent_name = intent["intent"]["name"]

	response = get_mongo_response(username=username,intent=intent_name)

	if type(response) == type(list()): return random.choice(response)
	else : return response


@app.route('/api/data',methods=['POST'])
def data():
	msg = str(request.get_data(),"utf-8")
	msg = json.loads(msg)
	questions = msg["questions"]
	answers = msg["answers"]
	intent = msg["intent"]
	username = msg["username"]
	if username == 'hybridx':
		if not check_file_exists(username) : save_file_data(username)
		training_data = load_file_data(username)
		if type(questions) == type(list()):
			for i in questions:
				training_data["rasa_nlu_data"]["common_examples"].append({"intent":intent,"text":i})
		else:
			training_data["rasa_nlu_data"]["common_examples"].append({"intent":intent,"text":questions})

		save_file_data(username=username,data=training_data)

		answers_data = {"intent":intent,"conversation":answers}
		status = save_data_mongo(username,answers_data)
		if status == True:
			response = {"status":"ok","response":"Data Saved"}
		else:
			response = {"status":"error","response":str(status)}
		return jsonify(response)
	else:
		response = {"status":"error","response":"Invalid user"}
		return jsonify(response)


@app.route('/app/data/create',methods=['POST'])
def create():
	try:
		msg = str(request.get_data(),"utf-8")
		msg = json.loads(msg)
		answers = msg["answers"]
		intent = msg["intent"]
		username = msg["username"]
		questions = msg["questions"]
		if not check_file_exists(username) : save_file_data(username=username)
		data = load_file_data(username)
		if type(questions) == type(list()):
			for i in questions:
				data["rasa_nlu_data"]["common_examples"].append({"intent":intent,"text":i})
		else:
			data["rasa_nlu_data"]["common_examples"].append({"intent":intent,"text":questions})

		response = save_file_data(username=username,data=data)

		answers_data = {"intent":intent,"conversation":answers}
		status = save_data_mongo(username,answers_data)


		if status == True:
			response = {"status":"ok","response":"Data Saved"}
		else:
			response = {"status":"error","response":str(status)}
		return jsonify(response)
	except Exception as e:
		response = {"status":"error","response":"Error creating user data"}
		return jsonify(response)


@app.route('/app/data/update',methods=['POST'])
def update_data():
	try:
		msg = str(request.get_data(),"utf-8")
		msg = json.loads(msg)
		questions = msg["questions"]
		answers = msg["answers"]
		intent = msg["intent"]
		username = msg["username"]

		data = load_file_data(username)
		
		if type(questions) == type(list()):
			data['rasa_nlu_data']['common_examples'] = [{"intent":intent,"text":i} for i in questions]
		else:
			data['rasa_nlu_data']['common_examples'] = [{"intent":intent,"text":questions}]

		save_file_data(username=username,data=data)

		update_mongo_data(username=username, intent=intent, answers=answers)

		response = {"status":"ok","response":"Data Updated"}
		return jsonify(response)
	except Exception as e:
		response = {"status":"error","response":"Data adding failed"}
		return jsonify(response)



@app.route('/app/data/remove',methods=['POST'])
def remove():
	try:
		msg = str(request.get_data(),"utf-8")
		msg = json.loads(msg)
		intent = msg["intent"]
		username = msg["username"]
		data = load_file_data(username)
		data['rasa_nlu_data']['common_examples'] = [i for i in data['rasa_nlu_data']['common_examples'] if i["intent"] != intent]
		save_file_data(username=username,data=data)
		remove_data_mongo(username=username,intent=intent)
		response = {"status":"ok","response":"Intent Removed"}
		return jsonify(response)
	except Exception as e:
		response = {"status":"error","response":"Request Failed"}
		return jsonify(response)



@app.route('/app/data/read_all_intents',methods=['POST'])
def read():
	msg = str(request.get_data(),"utf-8")
	msg = json.loads(msg)
	intent = msg["intent"]
	username = msg["username"]
	return jsonify(get_all_intents(username))

@app.route('/app/data/get_intent_data',methods=['POST'])
def intent_data():
	msg = str(request.get_data(),"utf-8")
	msg = json.loads(msg)
	intent = msg["intent"]
	username = msg["username"]
	return jsonify(get_intent_data(username, intent))


@app.route('/chatbot',methods=['POST'])
@cross_origin(supports_credentials=True)
def index_test():
	# The received text 
	text = str(request.get_data(),"utf-8")
	text = json.loads(text)
	text = text["text"]

	# Finding the intent of the text 
	intent = json.loads(get_intent(text))
	intent_name = intent['intent']['name']
	if intent_name == 'function':
		reply = function_response(text)
	else:
		reply =  get_mongo_response(username="original",intent=intent_name)
	if type(reply) == type(list()):
		reply = random.choice(reply)
		conversations.insert({"Bot": str(reply),"User":str(text),"intent":intent_name,"extra_data":str(intent)})
		return reply
	else:
		conversations.insert({"Bot": str(reply),"User":str(text),"intent":intent_name,"extra_data":str(intent)})
		return reply

def function_response(text):
	#url = "http://127.0.0.1:5500/function"
	#text = {"text":text}
	#r = requests.post(url,json=text)
	#return json.loads(r.text)["text"]
	return "Working on this :)"

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000,debug=True)
