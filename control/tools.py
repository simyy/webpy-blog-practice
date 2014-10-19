#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import urllib2

def downlod(hrefs=[], savepath='static/', saveprefix='' , savesuffix=''):
    for href in hrefs:
        data = urllib2.urlopen(href).read()
        imgname = href.split('/')[-1]
        if saveprefix != '':
            imgname = saveprefix + imgname
        if savesuffix != '':
            imgname = imgname + savesuffix
        f = file(savepath + imgname, 'wb')
        f.write(data)
        f.close()

if __name__ == '__main__':
    downlod(hrefs=['http://images.cnitblog.com/blog/452899/201410/191236254192949.jpg'],
            savepath='', saveprefix='111_', savesuffix='_22')