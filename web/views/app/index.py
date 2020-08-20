# -*- coding:utf-8 -*-

##########################################################################

from flask.views import MethodView
from flask import render_template, request

from web.views.app import view
from web.session import getSession

##########################################################################

class AppIndex(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        pkg = getSession('pkg')
        fileName = getSession('fileName')

        return render_template(self.template_name, pkg=pkg, fileName=fileName)


appindex = AppIndex.as_view('index', template_name='app/index.jinja')
view.add_url_rule('index', view_func=appindex)
