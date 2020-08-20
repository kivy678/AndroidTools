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

from web.session import getSession

from util.fsUtils import Join

##########################################################################

sp = getSharedPreferences(SHARED_PATH)
SAMPLE_DIR = sp.getString('SAMPLE_DIR')

##########################################################################


class Decomplier(MethodView):
    def get(self, mode=''):
        f = f'fetch_{mode}'

        if False == hasattr(self, f):
            return redirect('/app/index')

        return getattr(self, f)()

    def fetch_jadx(self):
        fileName = getSession('fileName')
        runJadxDecode(Join(SAMPLE_DIR, fileName))

        return "Jadx 완료"

    def fetch_androg(self):
        fileName = getSession('fileName')
        runAndrogDecode(Join(SAMPLE_DIR, fileName))

        return "안드로가드 완료"


decmp = Decomplier.as_view('decmp')
view.add_url_rule('decmp/<mode>', view_func=decmp)
