# -*- coding:utf-8 -*-

##########################################################################

from flask.views import MethodView
from flask import render_template, request
from flask import redirect, url_for

from web.views.app import view

from module.mobile.AppManager.debug import debugger

from common import getSharedPreferences
from webConfig import SHARED_PATH

from util.fsUtils import Join

##########################################################################

sp = getSharedPreferences(SHARED_PATH)
SAMPLE_DIR = sp.getString('SAMPLE_DIR')

##########################################################################

class AppDebug(MethodView):
    def post(self):
        for app in request.form.getlist('AppName'):
            debugger(Join(SAMPLE_DIR, app), force=False)

        return redirect(url_for('/.'))


appdebug = AppDebug.as_view('debug')
view.add_url_rule('debug', view_func=appdebug)
