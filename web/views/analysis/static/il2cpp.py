# -*- coding:utf-8 -*-

##########################################################################

import pandas as pd

from flask.views import MethodView
from flask import render_template, request

from web.views.analysis import view_static

from module.mobile.Analysis.static.il2cpp import startCmp
from module.mobile.Analysis.static.il2cpp_view import view

from module.database import df_il2cpp
from module.database.structure import STATUS

from util.fsUtils import Join
from util.parser import JSON
from util.hash import getSHA256

from common import getSharedPreferences
from webConfig import SHARED_PATH

from web.cache import getCache

##########################################################################

sp                  = getSharedPreferences(SHARED_PATH)
DECODE_DIR          = sp.getString('DECODE_DIR')

##########################################################################

class IL2CPPAnalysis(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        f1, f2 = [Join(DECODE_DIR, v['fileName'], 'unzip') for k, v in getCache('analysis').items()]
        f3, _ = [Join(DECODE_DIR, v['fileName'], 'il2cpp') for k, v in getCache('analysis').items()]

        cmp_data, path = startCmp(f1, f2)
        view_data, save_data = view(cmp_data, f3)

        cmp1_path, cmp2_path = path
        for il2cpp in save_data:
            data = {'ref_id':getSHA256(cmp1_path), 'function': il2cpp.function, 'offset': il2cpp.offset, 'opcode': il2cpp.cmp1, 'cmp_ref': getSHA256(cmp2_path)}
            df_il2cpp.DATA_FRAME = df_il2cpp.DATA_FRAME.append(pd.Series(data), ignore_index=True)

            data = {'ref_id':getSHA256(cmp2_path), 'function': il2cpp.function, 'offset': il2cpp.offset, 'opcode': il2cpp.cmp2, 'cmp_ref': getSHA256(cmp1_path)}
            df_il2cpp.DATA_FRAME = df_il2cpp.DATA_FRAME.append(pd.Series(data), ignore_index=True)


        df_il2cpp.DATA_FRAME = df_il2cpp.DATA_FRAME[~df_il2cpp.DATA_FRAME.duplicated(['ref_id', 'offset'], keep='first')]

        df_il2cpp.saveCSV()


        return "<pre>" + view_data + "<pre>"


il2cpp = IL2CPPAnalysis.as_view('il2cpp', template_name='')
view_static.add_url_rule('il2cpp', view_func=il2cpp)
