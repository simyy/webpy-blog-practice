#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import web
import os
from control import page, tools, db
from jinja2 import Environment, FileSystemLoader

import sys
reload(sys)
sys.setdefaultencoding('utf8')

render = web.template.render('templates')

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
        res = db.get_posts()
        return render_template('index.html',list=res)




