# -*- coding:utf-8 -*-

##################################################################################################

import pandas as pd

from flask.views import MethodView
from flask import render_template, request

from web.views.tip import view

from common import getSharedPreferences
from webConfig import SHARED_PATH

from module.database import df_opcode

##################################################################################################


class TipOPCDE(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        return render_template(self.template_name, enter=df_opcode.DATA_FRAME)

    def post(self):
        sha256 = request.form.get('GetHash')
        pkg = request.form.get('GetPkg')
        func = request.form.get('GetFunc')
        opcode = request.form.get('GetOpcode')
        binary = request.form.get('GetBin')

        if (sha256 is '') and (pkg is '')           \
                          and (func is '')          \
                          and (opcode is '')        \
                          and (binary is ''):

            return "모든 값들을 입력 해주세요."

        data = {'pkg':          pkg,
                'func':         func,
                'opcode':       opcode,
                'binary':       binary}

        add_idx = pd.Series(data).rename(sha256)
        df_opcode.DATA_FRAME = df_opcode.DATA_FRAME.append(add_idx)
        #df_opcode.DATA_FRAME = df_opcode.DATA_FRAME[~df_opcode.DATA_FRAME.index.duplicated(keep='first')]

        df_opcode.saveCSV()


        return "OPCODE LIST 저장 완료"


tipOpcode_view = TipOPCDE.as_view('opcode', template_name='tip/opcode.jinja')
view.add_url_rule('opcode', view_func=tipOpcode_view)
