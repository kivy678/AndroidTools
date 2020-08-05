# -*- coding:utf-8 -*-

##########################################################################

import os

from flask.views import MethodView
from flask import render_template, request

from web.views.analysis import view

from module.mobile.Analysis.yara.yara_run import run

##########################################################################


class YaraEngine(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        data = run(os.path.join(r'C:\tmp\dump', '*'))

        return render_template(self.template_name, enter=data)


yr = YaraEngine.as_view('yara', template_name='analysis/yara.jinja')
view.add_url_rule('yara', view_func=yr)
