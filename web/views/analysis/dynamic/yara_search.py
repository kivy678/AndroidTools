# -*- coding:utf-8 -*-

##########################################################################

import os

from flask.views import MethodView
from flask import render_template, request

from web.views.analysis import view_dynamic

from module.mobile.Analysis.dynamic.yara.run import run

from common import getSharedPreferences
from webConfig import SHARED_PATH

from util.fsUtils import Join, Copy, PathSplit
from web.session import getSession

##########################################################################

sp                  = getSharedPreferences(SHARED_PATH)
ANALYSIS_DIR        = sp.getString('ANALYSIS_DIR')
FILTER_DIR        	= Join(ANALYSIS_DIR, 'filter')

##########################################################################

class YaraEngine(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self, rule):
        pkg = getSession('pkg')
        dump = []

        for path in run(pkg, rule):
            dump.append(path)

            Copy(path, Join(FILTER_DIR, PathSplit(path)[1]))

        return '<pre>' + '\n'.join(dump) + '</pre>'


yr = YaraEngine.as_view('yara', template_name='')
view_dynamic.add_url_rule('yara/<rule>', view_func=yr)
