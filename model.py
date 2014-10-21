#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import os
import sys

import web
from jinja2 import Environment,FileSystemLoader

from funbox import db

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
        res = db.getContent()
        print res
        return render_template("index.html", list=res)




