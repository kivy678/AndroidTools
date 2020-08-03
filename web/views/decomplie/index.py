# -*- coding:utf-8 -*-

##########################################################################

import glob

from flask.views import MethodView
from flask import render_template, request

from web.views.decomplie import view

from common import getSharedPreferences
from webConfig import SHARED_PATH

from module.mobile.app.install import installer
from module.mobile.app.debug import debugger

from module.mobile.Decomplie.baksmali import runDecode
from module.mobile.Decomplie.androg import runAndrogDecode

from util.fsUtils import Join

##########################################################################


class DecomplieIndex(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        return render_template(self.template_name)


class AppInstall(MethodView):
    def get(self):
        sp = getSharedPreferences(SHARED_PATH)
        wk_dir = sp.getString('WORKING_DIR')

        app_list = (path for path in glob.glob(Join(wk_dir, '*')))

        for _path in app_list:
            installer(_path)

        return "설치를 완료하였습니다."


class AppDebug(MethodView):
    def get(self):
        sp = getSharedPreferences(SHARED_PATH)
        wk_dir = sp.getString('WORKING_DIR')

        app_list = (path for path in glob.glob(Join(wk_dir, '*')))

        for _path in app_list:
            debugger(_path)

        return "디버깅모드로 변경하였습니다."


class AppWait(MethodView):
    def get(self):
        print(request.args)

        return "웨이트 모드로 변경하였습니다."


class AppDecomplie(MethodView):
    def get(self):
        sp = getSharedPreferences(SHARED_PATH)
        wk_dir = sp.getString('WORKING_DIR')

        app_list = (path for path in glob.glob(Join(wk_dir, '*')))
        menu = request.args['menu'].strip()

        if menu == "baksmali":
            for _path in app_list:
                runDecode(_path)
        elif menu == "androg":
            for _path in app_list:
                runAndrogDecode(_path)

        return "디컴파일 완료"


appindex = DecomplieIndex.as_view('index', template_name='decomplie/index.jinja')
view.add_url_rule('index', view_func=appindex)


applist = AppInstall.as_view('install')
view.add_url_rule('install', view_func=applist)


appdebug = AppDebug.as_view('debug')
view.add_url_rule('debug', view_func=appdebug)


appwait = AppWait.as_view('wait')
view.add_url_rule('wait', view_func=appwait)


appdecomp = AppDecomplie.as_view('decomp')
view.add_url_rule('decomp', view_func=appdecomp)
