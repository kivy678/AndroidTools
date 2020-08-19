# -*- coding:utf-8 -*-

##########################################################################

import glob

from flask.views import MethodView
from flask import render_template, request

from web.views.analysis import view


from module.mobile.Analysis.dynamic.dynamic_server import *
from module.mobile.Analysis.frida.memdump import getMemoryDump

from common import getSharedPreferences
from webConfig import SHARED_PATH

from util.fsUtils import Join

from web.cache import getCache

##########################################################################





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


class Frida(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        return render_template(self.template_name)



dynamic = DynamicAnalysis.as_view('dynamic')
view.add_url_rule('dynamic', view_func=dynamic)

mdump = MemoryDump.as_view('mdump')
view.add_url_rule('mdump', view_func=mdump)

frida = Frida.as_view('frida', template_name='analysis/frida.jinja')
view.add_url_rule('frida', view_func=frida)
