# -*- coding:utf-8 -*-

##########################################################################

from flask.views import MethodView
from flask import render_template, request

from web.views.analysis import view_dynamic

from module.mobile.Analysis.dynamic.server import dynamicServer

##########################################################################

class DynamicServer(MethodView):
    def get(self):
        dynamicServer()

        return "동적 서버 구동 완료"


server = DynamicServer.as_view('server')
view_dynamic.add_url_rule('server', view_func=server)
