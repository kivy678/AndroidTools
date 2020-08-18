# -*- coding:utf-8 -*-

##########################################################################

import glob

from flask.views import MethodView
from flask import render_template, request

from web.views.app import view

from module.mobile.Analysis.static.parseApp import setApplicationInfor

from common import getSharedPreferences
from webConfig import SHARED_PATH

from util.fsUtils import Join

from web.cache import getCache

##########################################################################

sp = getSharedPreferences(SHARED_PATH)
SAMPLE_DIR = sp.getString('SAMPLE_DIR')

##########################################################################

class StaticAnalysis(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        app_list = (path for path in glob.glob(Join(SAMPLE_DIR, '*')))

        return render_template(self.template_name, enter=app_list)


    def post(self):
        for app in request.form.getlist('appName'):
            setApplicationInfor(Join(SAMPLE_DIR, app))

        return getCache('pkg')


static = StaticAnalysis.as_view('static', template_name='app/static.jinja')
view.add_url_rule('static', view_func=static, methods=['POST', 'get'])
