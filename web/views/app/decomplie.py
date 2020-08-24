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
from module.mobile.AppManager.Decomplie.unity import *

from web.session import getSession

from util.fsUtils import Join

##########################################################################

sp = getSharedPreferences(SHARED_PATH)
SAMPLE_DIR = sp.getString('SAMPLE_DIR')
DECODE_DIR = sp.getString('DECODE_DIR')

##########################################################################


class Decomplier(MethodView):
    def get(self, mode=''):
        f = f'fetch_{mode}'

        if False == hasattr(self, f):
            return redirect('/app/index')

        fileName = getSession('fileName')
        return getattr(self, f)(fileName)


    def fetch_jadx(self, fileName):
        runJadxDecode(Join(SAMPLE_DIR, fileName))

        return "Jadx 완료"


    def fetch_androg(self, fileName):
        runAndrogDecode(Join(SAMPLE_DIR, fileName), fileName)

        return "안드로가드 완료"


    def fetch_il2cpp(self, fileName):
        runDecodeil2cpp(Join(DECODE_DIR, fileName, 'unzip'), fileName)

        return "il2cpp 완료"


    def fetch_mono(self, fileName):
        runDecodeMono(Join(DECODE_DIR, fileName, 'unzip'), fileName)

        return "mono 완료"

decmp = Decomplier.as_view('decmp')
view.add_url_rule('decmp/<mode>', view_func=decmp)
