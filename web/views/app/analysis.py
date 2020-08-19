# -*- coding:utf-8 -*-

##########################################################################

from flask.views import MethodView
from flask import render_template, request
from flask import redirect, url_for

from web.views.app import view

from module.mobile.AppManager.parseApp import setApplicationInfor

from common import getSharedPreferences
from webConfig import SHARED_PATH

from util.fsUtils import Join

##########################################################################

sp = getSharedPreferences(SHARED_PATH)
SAMPLE_DIR = sp.getString('SAMPLE_DIR')

##########################################################################

class BasisAnalysis(MethodView):
    def post(self):
        for app in request.form.getlist('AppName'):
            setApplicationInfor(Join(SAMPLE_DIR, app))

        return redirect(url_for('/.'))


basis = BasisAnalysis.as_view('analysis')
view.add_url_rule('analysis', view_func=basis, methods=['POST'])
