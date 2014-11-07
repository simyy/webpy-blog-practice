#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import web
from blog.urls import urls

#web.config.debug = False
init
app = web.application(urls, globals())

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'count': 0})
    web.config._session = session
else:
    session = web.config._session

def session_hook():
    web.ctx.session = session

app.add_processor(web.loadhook(session_hook))

def my_loadhook():
    web.header('Content-type', "text/html; charset=utf-8")
    print 'loadhook'

def my_unloadhook():
    print 'unloadhook'

if __name__ == "__main__":
    #timer.backgroundrunning(timer.tick, '', 3)
    #timer.backgroundrunning(timer.getmyblog(), '', 10)
    app.add_processor(web.loadhook(my_loadhook))
    app.add_processor(web.unloadhook(my_unloadhook))
    app.run()