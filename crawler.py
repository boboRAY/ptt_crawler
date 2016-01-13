# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import urllib2
from pymongo import MongoClient
# import re
import time
import random

client = MongoClient()
db = client.ptt


def get_one_article(url,cat):
    content = urllib2.urlopen(url)
    soup = BeautifulSoup(content, 'lxml')

    try:
        time_tag = soup.find('span', class_="article-meta-tag", text='時間')
        time = time_tag.next_sibling.get_text()
        title_tag = soup.find('span', class_="article-meta-tag", text='標題')
        title = title_tag.next_sibling.get_text()
        print title
    except:
        print 'article error', url
        return

    lines = soup.find('div', class_='bbs-screen bbs-content')
    content = ''
    for line in lines:
        if line.name is None and line != title:
            content += line

    rawpushes = soup.find_all('div', class_='push')
    pushes = []
    for push in rawpushes:
        p = push.find_all('span')
        if not p:
            continue
        pushdict = {'type': p[0].get_text(), 'id': p[1].get_text(), 'content': p[2].get_text()[2:], 'date': p[3].get_text()}
        pushes.append(pushdict)
    article = {'time': time, 'title': title, 'content': content, 'pushes': pushes, 'class': cat}
    articles = db.articles
    articles.insert_one(article)


def get_onepage_live_url(url):
    content = urllib2.urlopen(url)
    soup = BeautifulSoup(content, 'lxml')
    blocks = soup.find_all('div', class_='r-ent')
    urls = []
    for block in blocks:
        urlblock = block.find('a')
        if urlblock:
            url = 'https://www.ptt.cc/'+urlblock['href']
            urls.append(url)
    return urls


def next_page(url):
    content = urllib2.urlopen(url)
    soup = BeautifulSoup(content, 'lxml')
    nextbtn = soup.find('a', text='‹ 上頁')
    return 'https://www.ptt.cc/'+nextbtn['href']


cats = {'Gossiping': 'https://www.ptt.cc/bbs/Gossiping/index10308.html',
        'LoL': ' https://www.ptt.cc/bbs/LoL/index4047.html',
        'NBA': 'https://www.ptt.cc/bbs/NBA/index3444.html',
        'Baseball': 'https://www.ptt.cc/bbs/Baseball/index4491.html',
        'WomenTalk': 'https://www.ptt.cc/bbs/WomenTalk/index4274.html',
        'C_Chat': 'https://www.ptt.cc/bbs/C_Chat/index4665.html',
        'e_shopping': 'https://www.ptt.cc/bbs/e-shopping/index2896.html',
        'Stock': 'https://www.ptt.cc/bbs/Stock/index2799.html',
        'joke': 'https://www.ptt.cc/bbs/joke/index3268.html',
        'HatePolitics': 'https://www.ptt.cc/bbs/HatePolitics/index3572.html'
        }

for cat in cats:
    count = 0
    url = cats[cat]
    while count <= 1000:
        while True:
            try:
                urls = get_onepage_live_url(url)
                url = next_page(url)
                break
            except:
                time.sleep(1)
                print 'except1 ', url
                continue
        for link in urls:
            while True:
                try:
                    get_one_article(link,cat)
                    count += 1
                    break
                except urllib2.HTTPError, err:
                    print 'except2 ', link
                    t = random.randint(1, 5)
                    time.sleep(t)
