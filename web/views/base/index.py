# -*- coding:utf-8 -*-

##################################################################################################

from flask.views import MethodView
from flask import render_template

from web.views.base import view

##################################################################################################


class IndexPage(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        return render_template(self.template_name)


index_page = IndexPage.as_view('', template_name='index.jinja')
view.add_url_rule('', view_func=index_page)
