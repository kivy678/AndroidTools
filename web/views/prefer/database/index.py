# -*- coding:utf-8 -*-

##################################################################################################

from flask.views import MethodView
from flask import render_template

from web.views.prefer import view_db

##################################################################################################


class DatabaseIndex(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        return render_template(self.template_name)


index = DatabaseIndex.as_view('index', template_name='prefer/database/index.jinja')
view_db.add_url_rule('index', view_func=index)
