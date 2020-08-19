# -*- coding:utf-8 -*-

##########################################################################

from flask.views import MethodView
from flask import render_template, request
from flask import redirect, url_for

from web.views.app import view

from common import getSharedPreferences
from webConfig import SHARED_PATH

from module.mobile.AppManager.Decomplie.jadx import runJadxDecode
from module.mobile.AppManager.Decomplie.androg import runAndrogDecode

from util.fsUtils import Join

##########################################################################

sp = getSharedPreferences(SHARED_PATH)
SAMPLE_DIR = sp.getString('SAMPLE_DIR')

##########################################################################

class JadxDecmp(MethodView):
    def post(self):
        for app in request.form.getlist('AppName'):
            runJadxDecode(Join(SAMPLE_DIR, app))

        return redirect(url_for('/.'))


class AndrogDecmp(MethodView):
    def post(self):
        for app in request.form.getlist('AppName'):
            runAndrogDecode(Join(SAMPLE_DIR, app))

        return redirect(url_for('/.'))


jdax = JadxDecmp.as_view('decmp/jadx')
view.add_url_rule('decmp/jadx', view_func=jdax)

androg = AndrogDecmp.as_view('decmp/androg')
view.add_url_rule('decmp/androg', view_func=androg)
