import pymongo
from pymongo import MongoClient

url = 'mongodb+srv://ggrass1585:password@cluster0.eo9bh.mongodb.net'
client = pymongo.MongoClient(url)
db = client['blog']
