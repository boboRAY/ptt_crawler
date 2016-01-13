# -*- coding: UTF-8 -*-
from pymongo import MongoClient


# client = MongoClient('140.112.107.119', 22222)
client = MongoClient()
db = client.ptt

article = db.articles.find_one()

print article['content']
