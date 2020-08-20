# -*- coding:utf-8 -*-

################################################################################

from flask.views import MethodView
from flask import render_template

from web.views.analysis import view_dynamic
from module.mobile.Analysis.dynamic.trace import straceStart

from web.session import getSession

################################################################################

class StraceDump(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        pkg = getSession('pkg')
        straceStart(pkg)

        return "덤프"


strace = StraceDump.as_view('strace', template_name='')
view_dynamic.add_url_rule('strace', view_func=strace)
