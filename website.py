#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import web
import model
from control import timer

urls = (
    '/','model.index',
    '/image', 'model.image'
)

if __name__ == "__main__":
    app = web.application(urls, globals())
    #timer.backgroundrunning(timer.tick, '', 3)
    app.run()