import json
import pymongo

mongodb = pymongo.MongoClient(username="admin",password="root",authSource="admin")
collection = mongodb.master.original

with open('data.json') as fp:
	data = json.load(fp)
	for i in data['ChatData']:
		collection.insert(i)

print('********************DONE***********************')