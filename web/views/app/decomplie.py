# -*- coding:utf-8 -*-

##########################################################################

import pandas as pd

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

from util.fsUtils import Join, PathSplit, FileSize
from util.hash import getSHA256

from module.database import df_unity
from module.database.structure import STATUS

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
        il2cpp_path     = runDecodeil2cpp(Join(DECODE_DIR, fileName, 'unzip'), fileName)

        parent_sha256   = getSHA256(Join(SAMPLE_DIR, fileName))
        sha256          = getSHA256(il2cpp_path)
        fSize           = FileSize(il2cpp_path)
        libName         = PathSplit(il2cpp_path)[1]

        data = {'fileName': libName, 'fileSize': fSize, 'build': 'il2cpp', 'parent': parent_sha256, 'status': STATUS.INIT.value}
        add_idx = pd.Series(data).rename(sha256)
        df_unity.DATA_FRAME = df_unity.DATA_FRAME.append(add_idx)
        df_unity.DATA_FRAME = df_unity.DATA_FRAME[~df_unity.DATA_FRAME.duplicated(keep='first')]

        df_unity.saveCSV()

        return "il2cpp 완료"


    def fetch_mono(self, fileName):
        il2cpp_path     = runDecodeMono(Join(DECODE_DIR, fileName, 'unzip'), fileName)

        parent_sha256   = getSHA256(Join(SAMPLE_DIR, fileName))
        sha256          = getSHA256(il2cpp_path)
        fSize           = FileSize(il2cpp_path)
        libName         = PathSplit(il2cpp_path)[1]

        data = {'fileName': libName, 'fileSize': fSize, 'build': 'mono', 'parent': parent_sha256, 'status': STATUS.INIT.value}
        add_idx = pd.Series(data).rename(sha256)
        df_unity.DATA_FRAME = df_unity.DATA_FRAME.append(add_idx)
        df_unity.DATA_FRAME = df_unity.DATA_FRAME[~df_unity.DATA_FRAME.duplicated(keep='first')]

        df_unity.saveCSV()

        return "mono 완료"

decmp = Decomplier.as_view('decmp')
view.add_url_rule('decmp/<mode>', view_func=decmp)
