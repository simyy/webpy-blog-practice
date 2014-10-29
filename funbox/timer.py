#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import time

from apscheduler.schedulers.background import BackgroundScheduler

'''
like crontab in linx, this is a python timer
'''

def tick():
    f = open('/s/log/test.log', 'w')
    f.write(time.ctime())
    f.close()
    print(time.ctime())

class timer:
    '''
    process = timer(function, [para1,para2,...], intervalseconds)
    process.run()
    '''
    def __init__(self, func, paras, seconds, id):
        self.func = func
        self.paras = paras
        self.time = seconds
        self.id = id
        self.scheduler = None
        self.setTimer()

    def setTimer(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.func, 'interval', seconds=self.time, id=self.id)

    def add_job(self, func, seconds, id):
        self.scheduler.add_job(func, 'interval', seconds, id)

    def remove_job(self, id):
        self.scheduler.remove_job(id)


    def run(self):
        self.scheduler.start()

def backgroundrunning(func=tick, args='', time=3, id='default'):
    a = timer(func, args, time, id)
    a.run()

if __name__ == '__main__':
    pass