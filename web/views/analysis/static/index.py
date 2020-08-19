# -*- coding:utf-8 -*-

##########################################################################

from flask.views import MethodView
from flask import render_template

from web.views.analysis import view_static

##########################################################################


class StaticIndex(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        return render_template(self.template_name)


index = StaticIndex.as_view('index', template_name='analysis/static/index.jinja')
view_static.add_url_rule('index', view_func=index)
