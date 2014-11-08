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


class index:
    def GET(self):
        data = web.input(num='1')
        print data.num
        db.query(('select * from article limit %s, 2')% (2*(int(data.num)-1)))
        articles = db.fetchAllRows()
        if len(articles) == 0:
            return 'error'
        db.query('select name,num from tag')
        tags = db.fetchAllRows()
        print tags
        return render_template("index.html", articles=articles, tags=tags)


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
            if not username:
                return web.redirect('/login')
        except Exception as e:
            return web.redirect('/login')
        ''' get tag '''
        db.query('select * from tag')
        res = db.fetchAllRows()
        if res == None:
            res = []
        return render_template("edit.html")
    def POST(self):
        data = web.input(title='', contents='',tag='')
        ''' update tag '''
        for tag in data.tag.split(';'):
            db.query('select name from tag')
            res = db.fetchAllRows()
            if len(tag) == 0:
                continue
            if (tag,) not in res:
                db.insert('insert into tag (name, num) values ("%s",1)'%tag)
            else:
                db.query('select id,num from tag where name="%s"'%tag)
                res = db.fetchOneRow()
                print res
                db.update('update tag set num=%d where id=%d'%((res[1]+1),res[0]))
        ''' update article '''
        db.query('select * from article where title="%s"'%data.title)
        res = db.fetchOneRow()
        if res == None:
            res = db.insert('insert into article (title, content, tag) values (\'%s\', \'%s\', \'%s\')'%(data.title, data.contents, data.tag))
            if not res:
                web.redirect('/edit')
            return 'success'
        return 'repeated title'


class login:
    def GET(self):
        return render_template("login.html")
    def POST(self):
        session = web.ctx.session
        data = web.input(email='', passwd='')
        if data.email != '' and data.passwd != '':
            db.query('select userpasswd from user where username=\'%s\''%data.email)
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




