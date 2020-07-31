# -*- coding:utf-8 -*-

##########################################################################

import glob

from flask.views import MethodView
from flask import render_template

from web.views.decomplie import view

from common import getSharedPreferences
from webConfig import SHARED_PATH

from util.fsUtils import Join

from module.mobile.app.install import installer
from module.mobile.app.debug import debugger

##########################################################################


class DecomplieIndex(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        return render_template(self.template_name)


class AppInstall(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        sp = getSharedPreferences(SHARED_PATH)
        wk_dir = sp.getString('WORKING_DIR')

        app_list = (path for path in glob.glob(Join(wk_dir, '*')))

        for _path in app_list:
            installer(_path)

        return "설치를 완료하였습니다."


class AppDebug(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        sp = getSharedPreferences(SHARED_PATH)
        wk_dir = sp.getString('WORKING_DIR')

        app_list = (path for path in glob.glob(Join(wk_dir, '*')))

        for _path in app_list:
            debugger(_path)

        return "디버깅모드로 변경하였습니다."


appindex = DecomplieIndex.as_view('index', template_name='decomplie/index.jinja')
view.add_url_rule('index', view_func=appindex)


applist = AppInstall.as_view('install', template_name='')
view.add_url_rule('install', view_func=applist)


appdebug = AppDebug.as_view('debug', template_name='')
view.add_url_rule('debug', view_func=appdebug)
