# -*- coding:utf-8 -*-

##########################################################################

from flask.views import MethodView
from flask import render_template, request

from web.views.analysis import view_static

from module.mobile.Analysis.static.il2cpp import startCmp
from module.mobile.Analysis.static.il2cpp_view import view

from util.fsUtils import Join

from common import getSharedPreferences
from webConfig import SHARED_PATH

from web.cache import getCache

##########################################################################

sp                  = getSharedPreferences(SHARED_PATH)
DECODE_DIR          = sp.getString('DECODE_DIR')

##########################################################################

class IL2CPPAnalysis(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        f1, f2 = [Join(DECODE_DIR, v['fileName'], 'unzip') for k, v in getCache('analysis').items()]
        f3, _ = [Join(DECODE_DIR, v['fileName'], 'il2cpp') for k, v in getCache('analysis').items()]

        return "<pre>" + view(startCmp(f1, f2), f3) + "<pre>"


il2cpp = IL2CPPAnalysis.as_view('il2cpp', template_name='')
view_static.add_url_rule('il2cpp', view_func=il2cpp)
