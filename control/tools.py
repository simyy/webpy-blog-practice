#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import urllib2

def downlod(hrefs=[], savepath='static/', saveprefix='' , savesuffix=''):
    for href in hrefs:
        data = urllib2.urlopen(href).read()
        imgname = href.splist('/')[-1]
        if saveprefix != '':
            imgname = saveprefix + imgname
        if savesuffix != '':
            imgname = imgname + savesuffix
        f = file(savepath + imgname, 'wb')
        f.write(data)
        f.close()

if __name__ == '__main__':
    downlod()