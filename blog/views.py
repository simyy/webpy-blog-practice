#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import os
import sys
import web
from decorator import addUrl
from markdown import markdown
from jinja2 import Environment,FileSystemLoader
#from website import session
from db import db
#from blog.log import log

reload(sys)
sys.setdefaultencoding('utf8')

# jinja2模板加载
def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    print os.path.join(os.path.abspath(os.path.join(os.path.dirname("__file__"))), 'templates')

    jinja_env = Environment(
            #loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
            loader=FileSystemLoader(os.path.join(os.path.abspath(os.path.join(os.path.dirname("__file__"))), 'templates')),
            extensions=extensions,
            )
    jinja_env.globals.update(globals)
    #jinja_env.update_template_context(context)
    return jinja_env.get_template(template_name).render(context)

@addUrl('/')
class index:
    def GET(self):
        db.query('select * from articletab limit 0,2')
        res = db.fetchAllRows()
        #print res
        return render_template("index.html", articles=res)

class test:
    def GET(self):
       session = web.ctx.session
       print 'session', session
       session.count += 1
       return 'Hello, %s!' % session.count

class edit:
    def GET(self):
        try:
            session = web.ctx.session
            username = session.username
            print username,'123'
            if not username:
                return web.redirect('/login')
        except Exception as e:
            return web.redirect('/login')
        return render_template("edit.html")
    def POST(self):
        data = web.input(title='', summary='', contents='',tag='')

        res = db.insert('insert into articletab (Author, Title, Content, ArticleType, Summary) values (\'%d\', \'%s\', \'%s\', \'%d\', \'%s\')'%(1, data.title, data.contents, 1, data.summary))
        print res
        if not res:
            web.redirect('/edit')
        return 'success'

class login:
    def GET(self):
        return render_template("login.html")
    def POST(self):
        session = web.ctx.session
        data = web.input(email='', passwd='')
        if data.email != '' and data.passwd != '':
            db.query('select userPwd from usertab where userName=\'%s\''%data.email)
            res = db.fetchOneRow()
            print res
            if res != None and res[0] == data.passwd:
                session.loggedin = True
                session.username = data.email
                return web.seeother("/edit")
            else:
                return web.redirect('/login')

class loginout:
    def GET(self):
        web.ctx.session.kill()
        return web.redirect('/login')




