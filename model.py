#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import web
from control import page, getimage
import sys
reload(sys)
sys.setdefaultencoding('utf8')

render = web.template.render('templates')

class index:
    def GET(self):
        myPage = page.page()
        return render.index(myPage.parse(), getimage.getImg())

class image:
    def GET(self):
        return render.image()


