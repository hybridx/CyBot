from flask import Flask,request,render_template,jsonify
import requests
import mods
import json

app = Flask(__name__)

@app.route('/function',methods=['POST'])
def index():
	text = str(request.get_data()).encode("utf-8")
	text = json.loads(text)
	text = text["text"]
	print(text)
	pa.mods.query(text, pa)
	return json.dumps({"text": pa.text})

class func(object):
	def run(self):
		self.mods = mods.mods()
		self.text = ""
		app.run(host='0.0.0.0',port=5500,debug=True)

		# while True:
		# 	ot = self.stt.listen()
		# 	#f=open("pr", "w")
		# 	#f.write(ot)
		# 	#f.close()
		# 	print(ot)
		# 	self.mods.query(ot, self)
		# 	print(self.tts.txt)
		# 	self.tts.say(self.tts.txt)
		# 	self.tts.txt = ""

if __name__ == "__main__":
	pa = func()
	pa.run()