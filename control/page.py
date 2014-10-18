#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import urllib2

from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf8')

site = 'http://www.cnblogs.com/'

class page():
    '''
    '''
    def __init__(self, href=site):
        page.href = href
        page.doc = ''
        page.title = ''
        self.loadPage()

    def loadPage(self):
        try:
            self.doc = urllib2.urlopen(site).read()
        except Exception as e:
            print 'urlopen error: ',e
            return ''

    def parse(self):
        res = []
        soup = BeautifulSoup(self.doc, from_encoding='gbk')
        f = open('page.log', 'w+')
        f.write(soup.prettify())
        f.close()
        #print soup.title.string
        newscontents = soup.findAll(name='div', attrs={'class':'post_item'})
        for news in newscontents:
            tmp = []
            content = news.find(name='h3')
            title = content.string
            #print title
            href = content.find('a').get('href')
            #print href
            summary = news.find(name='p').text
            #print summary
            tmp.append(title)
            tmp.append(href)
            tmp.append(summary)
            res.append(tmp)
        return res


if __name__ == '__main__':
    a = page()
    print a.parse()