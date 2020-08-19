# -*- coding:utf-8 -*-

##########################################################################

from flask.views import MethodView
from flask import render_template, request

from web.views.app import view

from module.mobile.AppManager.installer import *

from common import getSharedPreferences
from webConfig import SHARED_PATH

from util.fsUtils import Join

##########################################################################

sp = getSharedPreferences(SHARED_PATH)
SAMPLE_DIR = sp.getString('SAMPLE_DIR')

##########################################################################

class AppInstall(MethodView):
    def post(self):
        for app in request.form.getlist('AppName'):
            cmdInstall(Join(SAMPLE_DIR, app))

        return "설치를 완료하였습니다."


class AppUnInstall(MethodView):
    def post(self):
        cmdUninstall()

        return "삭제를 완료하였습니다."


install = AppInstall.as_view('install')
view.add_url_rule('install', view_func=install, methods=['POST'])

uninsall = AppUnInstall.as_view('uninstall')
view.add_url_rule('uninstall', view_func=uninsall, methods=['POST'])
