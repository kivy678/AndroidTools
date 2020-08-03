# -*- coding:utf-8 -*-

##########################################################################

import glob

from flask.views import MethodView
from flask import render_template, request

from web.views.analysis import view

from module.mobile.Analysis.static.parseApp import setApplicationInfor
from module.mobile.Analysis.dynamic.dynamic_server import *
from module.mobile.Analysis.frida.memdump import getMemoryDump

from common import getSharedPreferences
from webConfig import SHARED_PATH

from util.fsUtils import Join

from web.cache import getCache

##########################################################################


class StaticAnalysis(MethodView):
    def get(self):
        sp = getSharedPreferences(SHARED_PATH)
        wk_dir = sp.getString('WORKING_DIR')

        app_list = (path for path in glob.glob(Join(wk_dir, '*')))

        for _path in app_list:
            setApplicationInfor(_path)

        return "정적 분석 완료"


class DynamicAnalysis(MethodView):
    def get(self):
        menu = request.args['menu'].strip()
        if menu == "run":
            dynamicServer()
            return "동적 분석 준비 완료"

        elif menu == "jdb":
            #jdbStart()
            return "JDB 준비 완료"


class MemoryDump(MethodView):
    def get(self):
        pkgName = getCache('pkg').strip()
        getMemoryDump(pkgName)

        return "메모리 덤프 완료"



class TEST(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        return "TEST"


static = StaticAnalysis.as_view('static')
view.add_url_rule('static', view_func=static)

dynamic = DynamicAnalysis.as_view('dynamic')
view.add_url_rule('dynamic', view_func=dynamic)

mdump = MemoryDump.as_view('mdump')
view.add_url_rule('mdump', view_func=mdump)

test = TEST.as_view('test', template_name='')
view.add_url_rule('test', view_func=test)
