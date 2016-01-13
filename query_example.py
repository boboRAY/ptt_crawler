# -*- coding: UTF-8 -*-
from pymongo import MongoClient
#first import pymongo

client = MongoClient('140.112.107.119', 22222) #connect to db server 裡面變數不要改
db = client.ptt #使用 ptt table

#以上就照抄就好，這樣才能使用正確的 DB

articles = db.articles.find() #抓出全部的文章，存成一個 list，每一格是一個 dictionary


for article in articles:
    # article 長得像這樣
    #
    #{'title' : '這是標題',
    # 'content' : '內文內文內文',
    # 'time' : 'ed Jan 13 22:59:44 2016',
    # 'class' : '英文版名(ex: WomenTalk),
    # 'pushes' :  [
    #             {
    #                             "content" : "正在用！",
    #                             "date" : "01/13 23:00\n",
    #                             "type" : "推 ",
    #                             "id" : "Chloe1990"
    #                         },
    #             {
    #                             "content" : "我有買電暖蛋,但撐不久,說明書上說只能撐2hr",
    #                             "date" : "01/13 23:01\n",
    #                             "type" : "→ ",
    #                             "id" : "estatevinger"
    #                         }]
    # }
    # pushes 取出來是一個 list，每一格是一個推文的 dict

    # 舉例
    print article['content']
    # 這裡會 print 出內文，也就是 內文內文內文

