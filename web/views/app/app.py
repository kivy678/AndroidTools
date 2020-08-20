# -*- coding:utf-8 -*-

##########################################################################

import glob

from flask.views import MethodView
from flask import render_template, request
from flask import redirect, url_for

from web.views.app import view

from common import getSharedPreferences
from webConfig import SHARED_PATH

from util.fsUtils import Join, PathSplit

from module.mobile.AppManager.installer import *
from module.mobile.AppManager.parseApp import setApplicationInfor
from module.mobile.AppManager.debug import debugger

from web.session import getSession

##########################################################################

sp = getSharedPreferences(SHARED_PATH)
SAMPLE_DIR = sp.getString('SAMPLE_DIR')

##########################################################################


class AppBasis(MethodView):
    def get(self, mode=''):
        f = f'fetch_{mode}'

        if False == hasattr(self, f):
            return redirect('/app/index')

        return getattr(self, f)()

    def post(self, mode=''):
        f = f'fetch_{mode}'

        if False == hasattr(self, f):
            return redirect('/app/index')

        return getattr(self, f)()

    def fetch_list(self):
        app_list = (PathSplit(path)[1] or path in glob.glob(Join(SAMPLE_DIR, '*')))

        return render_template('app/list.jinja', enter=app_list)

    def fetch_analysis(self):
        for app in request.form.getlist('AppName'):
            setApplicationInfor(Join(SAMPLE_DIR, app))

        return "기본 분석 완료"

    def fetch_install(self):
        fileName = getSession('fileName')
        cmdInstall(Join(SAMPLE_DIR, fileName))

        return "설치 완료"

    def fetch_uninstall(self):
        pkg = getSession('pkg')
        cmdUninstall(pkg)

        return "삭제 완료"

    def fetch_debug(self):
        fileName = getSession('fileName')
        debugger(Join(SAMPLE_DIR, fileName), force=False)

        return "디버깅 모드 변환 완료"


basis = AppBasis.as_view('')
view.add_url_rule('/<mode>', view_func=basis)
