#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import os
import sys
import web
import time
from markdown import markdown
from jinja2 import Environment,FileSystemLoader
from db import db
import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')

def auth():
    try:
        session = web.ctx.session
        username = session.username
        if not username:
            return web.redirect('/login')
    except Exception as e:
        print e
        return web.redirect('/login')

def Auth(func):
    def wrapped(param):
        try:
            session = web.ctx.session
            username = session.username
            if not username:
                return web.redirect('/login')
        except Exception as e:
            print e
            return web.redirect('/login')
        else:
            func(param)
    return wrapped

# jinja2模板加载
def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    #print os.path.join(os.path.abspath(os.path.join(os.path.dirname("__file__"))), 'templates')

    jinja_env = Environment(
            #loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
            loader=FileSystemLoader(os.path.join(os.path.abspath(os.path.join(os.path.dirname("__file__"))), 'templates')),
            extensions=extensions,
            )
    jinja_env.globals.update(globals)
    #jinja_env.update_template_context(context)
    return jinja_env.get_template(template_name).render(context)


class detail:
    def GET(self):
        id = web.input(id='').id
        if id == '':
            return 'no articles'
        db.query('select * from article where id=%d'%int(id))
        res = db.fetchOneRow()
        if len(res) < 1:
            return 'no articles'
        else:
            article = []
            for item in res:
                if item == res[2]:
                    article.append(markdown(item))
                    continue
                article.append(item)
            db.query('select name,num from tag')
            tags = db.fetchAllRows()
            db.query('select title from article limit 0,10')
            titles = db.fetchAllRows()
            return render_template("detail.html", articles=[article], tags=tags, titles=titles)

class index:
    def GET(self):
        data = web.input(num='1')
        db.query(('select * from article as p order by p.posttime desc limit %s, %s')% ((int(data.num)-1)*5, (int(data.num))*5))
        res = db.fetchAllRows()
        if len(res) < 1 and data.num == '1':
            articles = [(1,'hello','this is no articles!'),]
        elif len(res) < 1 and data.num != '1':
            db.query('select name,num from tag')
            tags = db.fetchAllRows()
            db.query('select title from article limit 0,10')
            titles = db.fetchAllRows()
            return render_template("nothing.html", tags=tags, titles=titles)
        else:
            articles = []
            for items in res:
                article = []
                for item in items:
                    if item == items[2]:
                        tmp = markdown(item)
                        if (data.num == '1') and (items == res[0]):
                            pass
                        else:
                            s = tmp.find('\n')
                            if s > 80:
                                tmp = BeautifulSoup.BeautifulSoup(tmp[0:80]).text
                            else:
                                tmp = BeautifulSoup.BeautifulSoup(tmp[0:s]).text
                        article.append(tmp)
                        continue
                    article.append(item)
                articles.append(article)
        db.query('select name,num from tag')
        tags = db.fetchAllRows()
        db.query('select title from article limit 0,10')
        titles = db.fetchAllRows()
        return render_template("index.html", articles=articles, tags=tags, titles=titles)

class test:
    def GET(self):
        if True:
            return render_template('index.html')
        session = web.ctx.session
        print 'session', session
        session.count += 1
        return 'Hello, %s!' % session.count


class edit:
    @Auth
    def GET(self):
        auth()
        ''' get tag '''
        print '123'
        db.query('select * from tag')
        res = db.fetchAllRows()
        if res == None:
            res = []
        return render_template("edit.html")
    def POST(self):
        auth()
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
            res = db.insert('insert into article (title, content, tag, posttime) values ("%s", "%s", "%s", "%s")'%(data.title, data.contents, data.tag, time.strftime('%Y-%m-%d %H:%M:%S')))
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




