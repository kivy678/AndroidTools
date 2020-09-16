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
        sha256      = request.form.get('GetHash')

        df_opcode.DATA_FRAME.loc[sha256, 'pkg']         = request.form.get('GetPkg')
        df_opcode.DATA_FRAME.loc[sha256, 'func']        = request.form.get('GetFunc')
        df_opcode.DATA_FRAME.loc[sha256, 'opcode']      = request.form.get('GetOpcode')
        df_opcode.DATA_FRAME.loc[sha256, 'binary']      = request.form.get('GetBin')
        df_opcode.DATA_FRAME.loc[sha256, 'engine']      = request.form.get('GetEngine')
        df_opcode.DATA_FRAME.loc[sha256, 'platform']    = request.form.get('GetPlatform')
        #df_opcode.DATA_FRAME = df_opcode.DATA_FRAME[~df_opcode.DATA_FRAME.index.duplicated(keep='first')]
        df_opcode.DATA_FRAME = df_opcode.DATA_FRAME[df_opcode.DATA_FRAME.index.notnull()]

        df_opcode.saveCSV()


        return "OPCODE LIST 저장 완료"


tipOpcode_view = TipOPCDE.as_view('opcode', template_name='tip/opcode.jinja')
view.add_url_rule('opcode', view_func=tipOpcode_view)
