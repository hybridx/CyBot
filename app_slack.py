from slackclient import SlackClient
from flask import Flask, request, Response, jsonify
import json
import requests

app = Flask(__name__)

SLACK_TOKEN = '---'
slack_client = SlackClient(SLACK_TOKEN)
slack_token = '---'


def send_message(channel_id, message,user):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username="Vitti",
        icon_emoji=':sansa:'
    )


@app.route('/slack',methods=['POST'])
def inbound():
	data = request.json
	if request.json.get('type') == 'url_verification':
		return request.json.get('challenge'),200

	if request.json.get('token') == slack_token:
		messaging_events = data.get('event')
		channel = messaging_events.get('channel')
		user = messaging_events.get('user')
		text = messaging_events.get('text')
		bot = messaging_events.get('bot_id')

	if 'subtype' not in data['event'].keys():
		url = "http://localhost:12345/chatbot"
		text = {"text" : text}
		reply = requests.post(url,json=text).text
		send_message(channel, reply, user)
	return Response(),200

@app.route('/',methods=['GET','POST'])
def test():
	return jsonify({'status':'ok'})

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=12345,debug=True)
