#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import urllib2

from bs4 import BeautifulSoup
from log import log
import sys
reload(sys)
sys.setdefaultencoding('utf8')

site = 'http://www.cnblogs.com/'

class page():
    '''
    import page

    result = page.page(href='www.baidu.com', parsefunc=parse())
    '''
    def __init__(self, href=site, parsefunc=None):
        self.href = href
        self.doc = ''
        self.parsefunc = parsefunc
        self.loadPage()

    def loadPage(self):
        try:
            self.doc = urllib2.urlopen(site).read()
        except Exception as e:
            print 'urlopen error: ',e
            return ''
        return self.parse(self.doc)

    def parse(self):
        self.loadPage()
        self.parsefunc(self.doc)

    def find(self, name='', attrs={}):
        soup = BeautifulSoup(self.doc, from_encoding='gbk')
        result = soup.findAll(name=name, attrs=attrs)


if __name__ == '__main__':
    a = page()
    print a.parse()