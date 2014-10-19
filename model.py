#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import web
from control import page, tools

import sys
reload(sys)
sys.setdefaultencoding('utf8')

render = web.template.render('templates')

class index:
    def GET(self):
        return render.index()

class image:
    def GET(self):
        return render.image()


