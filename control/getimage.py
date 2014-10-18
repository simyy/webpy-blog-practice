#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import urllib2
from bs4 import BeautifulSoup

site = 'http://www.cnblogs.com/'
path = '../static/image/name_img/'

def getImg():
    try:
        doc = urllib2.urlopen(site).read()
    except Exception as e:
        print 'urlopen error: ',e
        return ''
    dict = {}
    soup = BeautifulSoup(doc, from_encoding='gbk')
    newscontents = soup.findAll(name='div', attrs={'class':'post_item_body'})
    for item in newscontents:
        src = item.find(name='img')
        if src:
            imgSrc = src.get('src')
        else:
            imgSrc = ''
            continue
        print imgSrc
        name = item.find(name='a', attrs={'class':'lightblue'}).string
        print name
        dict[name] = imgSrc
    return dict

def downlod(imgDict):
    for name in imgDict:
        data = urllib2.urlopen(imgDict[name]).read()
        imgid = imgDict[name].split('/')[-1]
        if imgid.find('=') != -1:
            imgid = imgid.split('=')[-1] + '.jpg'
        print imgid
        f = file(path+imgid, 'wb')
        f.write(data)
        f.close()
        print name


if __name__ == '__main__':
    downlod(getImg())