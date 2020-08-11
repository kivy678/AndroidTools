# -*- coding:utf-8 -*-

##########################################################################

from flask.views import MethodView
from flask import render_template, request

from web.views.analysis import view

import elfformat

##########################################################################


class Disasm(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        return "<pre>" + '\n'.join([i for i in elfformat.parser(r"C:\tmp\libSecShell.so")]) + "<pre>"


format = Disasm.as_view('format', template_name='')
view.add_url_rule('format', view_func=format)
