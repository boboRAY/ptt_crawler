# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import urllib2
from pymongo import MongoClient
import re
import time
import random
import cookielib

client = MongoClient()
db = client.ptt


def get_one_article(url, cat):
    _cookset='over18=1; __utma=156441338.319066453.1448507855.1448507855.1448507855.1; __utmc=156441338; __utmz=156441338.1448507855.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
    _Opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    _Opener.addheaders = [('Cookie', _cookset)]
    request=_Opener.open(url)
    content = request.read()

    #content = urllib2.urlopen(url)
    soup = BeautifulSoup(content, 'lxml')


    try:
        time_tag = soup.find('span', class_="article-meta-tag", text='時間')
        time = time_tag.next_sibling.get_text()
        title_tag = soup.find('span', class_="article-meta-tag", text='標題')
        title = title_tag.next_sibling.get_text()
        print title
    except:
        print 'article error', url
        return False

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
    return True


def get_onepage_live_url(url):
    _cookset='over18=1; __utma=156441338.319066453.1448507855.1448507855.1448507855.1; __utmc=156441338; __utmz=156441338.1448507855.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
    _Opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    _Opener.addheaders = [('Cookie', _cookset)]
    request=_Opener.open(url)
    content = request.read()
    #content = urllib2.urlopen(url)
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
    _cookset='over18=1; __utma=156441338.319066453.1448507855.1448507855.1448507855.1; __utmc=156441338; __utmz=156441338.1448507855.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
    _Opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    _Opener.addheaders = [('Cookie', _cookset)]
    request=_Opener.open(url)
    content = request.read()
    #content = urllib2.urlopen(url)
    soup = BeautifulSoup(content, 'lxml')
    nextbtn = soup.find('a', text='‹ 上頁')
    return 'https://www.ptt.cc/'+nextbtn['href']




cats =  {'Gossiping':'https://www.ptt.cc/bbs/Gossiping/index10306.html'}


for cat in cats:
    count = 0
    url = cats[cat]
    while count <= 1000:
        while True:
            try:
                urls = get_onepage_live_url(url)
                url = next_page(url)
                break
            except urllib2.HTTPError as err:
                time.sleep(1)
                print 'except1 ',err , url
                continue
        for link in urls:
            while True and count <= 1000:
                try:
                    print count, cat
                    if get_one_article(link, cat):
                        count += 1
                    break
                except urllib2.HTTPError as err:
                    if err.code == 404:
                        break
                    print 'except2 ',err , link
                    t = random.randint(1, 5)
                    time.sleep(t)
