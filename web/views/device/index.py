# -*- coding:utf-8 -*-

##########################################################################

from flask.views import MethodView
from flask import render_template

from web.views.device import view

##########################################################################


class DEVICE_INDEX(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        return render_template(self.template_name)


device_index = DEVICE_INDEX.as_view('index', template_name='device/index.jinja')
view.add_url_rule('index', view_func=device_index)
