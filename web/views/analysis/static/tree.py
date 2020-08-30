# -*- coding:utf-8 -*-

##########################################################################

from flask.views import MethodView
from flask import render_template, request

from web.views.analysis import view_static

from module.mobile.Analysis.static.tree import startCmp

from util.fsUtils import Join

from common import getSharedPreferences
from webConfig import SHARED_PATH

from web.cache import getCache

##########################################################################

sp                  = getSharedPreferences(SHARED_PATH)
DECODE_DIR          = sp.getString('DECODE_DIR')

##########################################################################

class TreeAnalysis(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        f1, f2 = [Join(DECODE_DIR, v['fileName'], 'unzip') for k, v in getCache('analysis').items()]

        return "<pre>" + startCmp(f1, f2) + "<pre>"


tree = TreeAnalysis.as_view('tree', template_name='')
view_static.add_url_rule('tree', view_func=tree)
