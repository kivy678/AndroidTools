# -*- coding:utf-8 -*-

##########################################################################

from flask.views import MethodView
from flask import render_template, request

from web.views.app import view

from module.mobile.AppManager.set_wait import setDebug

from web.session import getSession

##########################################################################

class AppWait(MethodView):
    def get(self):
        mode = request.args['mode'].strip()
        if mode == "set":
            m = True
        elif mode == "clear":
            m = False

        setDebug(getSession('pkg'), m)

        return f"{mode} 모드를 변경하였습니다."


appwait = AppWait.as_view('wait')
view.add_url_rule('wait', view_func=appwait)
