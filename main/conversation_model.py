from rasa_nlu.model import Interpreter

import json

try:
	interpreter = Interpreter.load('./models/nlu/default/conversation')
except Exception as e:
	print("Error loading model",e)

def get_intent(msg):
	return json.dumps(interpreter.parse(u"{}".format(msg)),indent=2)