# -*- coding:utf-8 -*-

##########################################################################

from flask.views import MethodView
from flask import render_template, request

from web.views.app import view

##########################################################################

class DecomplieIndex(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        return render_template(self.template_name)


appindex = DecomplieIndex.as_view('index', template_name='app/index.jinja')
view.add_url_rule('index', view_func=appindex)
