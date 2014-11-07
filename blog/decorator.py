#!/usr/bin/env python
#-*- encoding:utf-8 -*-
from urls import urls
import os

def addUrl(url):
    print __file__
    def addView(func):
        def wrapper(*args, **kw):
            #print func.__name__
            urls.append(url)
            urls.append('blog.views.' + func.__name__)
            return func(*args, **kw)
        return wrapper
    return addView

if __name__ == '__main__':
    i = 123
