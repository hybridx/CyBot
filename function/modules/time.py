import datetime

words = ["time"]

def handle(text, ai):
	now = datetime.datetime.now()
	ai.text = "It is currently "+now.strftime("%I:%M %p")+" on my clock."

def isValid(text):
	keymatch = 0;
	for w in words:
		for t in text:
			if t == w:
				keymatch = keymatch + 1
	return keymatch