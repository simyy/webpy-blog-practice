#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import web
import MySQLdb

db = None
cursor = None

def dbconn():
    global db
    global cursor
    db = MySQLdb.connect("localhost","root","123123",charset='utf8')
    cursor = db.cursor()

def dbclose():
    db.close()

def getContent():
    dbconn()
    result = []
    try:
        sql = 'select * from test.myblog'
        n = cursor.execute(sql)
        if n > 0:
            result = cursor.fetchall()
        dbclose()
    except:
        dbclose()
        pass
    return result

def get_posts():
    return db.select('myblog')

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
    print getContent()