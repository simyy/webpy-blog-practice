#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import web
import datetime

db = web.database(dbn='mysql', db='test', user='root', pw='123123')

def new_post(title, content):
    db.insert('news', title=title, content=content, posted_on=datetime.datetime.utcnow())

def get_post(id):
    try:
        return db.select('news', where='id=$id', vars=locals())[0]
    except IndexError:
        return None

def get_posts():
    return db.select('news', order = 'id DESC')

def del_post(id):
    db.delete('news', where = 'id = $id', vars = locals())

def update_post(id, title, content):
    db.update('news', where='id = $id', vars=locals(), title=title, content=content)

if __name__ == '__main__':
    #new_post('test','test...')
    #print get_post(1)
    #res = get_posts()
    #for t in res:
    #    print t
    del_post(1)