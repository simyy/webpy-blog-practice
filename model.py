#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import os
import sys
import web
from jinja2 import Environment,FileSystemLoader

from funbox.db import db
#from funbox.log import log

reload(sys)
sys.setdefaultencoding('utf8')

render = web.template.render('templates')

# jinja2模板加载
def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
            extensions=extensions,
            )
    jinja_env.globals.update(globals)
    #jinja_env.update_template_context(context)
    return jinja_env.get_template(template_name).render(context)

class index:
    def GET(self):
        db.query('select * from articletab')
        res = db.fetchAllRows()
        print res
        return render_template("index.html", articles=res)

class test:
    def GET(self):
        return render_template("login.html")

class edit:
    def GET(self):
        return render_template("edit.html")
    def POST(self):
        data = web.input(title='', summary='', contents='')
        print data
        return data

class login:
    def GET(self):
        return render_template("login.html")
    def POST(self):
        data = web.input(email='', passwd='')
        if data.email != '' and data.passwd != '':
            db.query('select userPwd from usertab where userName=\'%s\''%data.email)
            res = db.fetchOneRow()
            if res != None and res[0] == data.passwd:
                return render_template("index.html")
            else:
                return web.redirect('/login')


