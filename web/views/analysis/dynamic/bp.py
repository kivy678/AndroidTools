# -*- coding:utf-8 -*-

##########################################################################

from flask.views import MethodView
from flask import render_template, request
from werkzeug.utils import secure_filename

from web.views.analysis import view_dynamic

from util.fsUtils import Join, DirCheck, Delete

from module.mobile.Analysis.dynamic.bp import *

from common import getSharedPreferences
from webConfig import SHARED_PATH

##########################################################################

sp                  = getSharedPreferences(SHARED_PATH)
ANALYSIS_DIR        = sp.getString('ANALYSIS_DIR')

ES_DIR              = Join(ANALYSIS_DIR, 'es')
DBG_BP              = {"ARM": "700020E1", "THUMB": "00BE", "X86": "CC"}
DBG_SIZE            = {"ARM": 4,          "THUMB": 2,      "X86": 1}

##########################################################################


class BREAK_POINT(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name


    def get(self):
        Delete(ES_DIR)
        DirCheck(ES_DIR)

        return render_template(self.template_name)


    def post(self):
        f = request.files['LogFileName']
        fileName = f.filename

        csv_path = Join(ES_DIR, secure_filename(fileName))
        f.save(csv_path)

        platform = request.form.get("platform")
        baseAddr = request.form.get("GetBase")

        setBP(csv_path, baseAddr, DBG_BP[platform], DBG_SIZE[platform])

        return "BP 완료"


class RESOTRE_POINT(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name


    def get(self):
        if restoreBP() is False:
            return "BP가 없습니다."

        return "BP 완료"


bp_view = BREAK_POINT.as_view('bp', template_name='analysis/dynamic/bp.jinja')
view_dynamic.add_url_rule('bp', view_func=bp_view, methods=['POST', 'get'])

rbp_view = RESOTRE_POINT.as_view('rbp', template_name='')
view_dynamic.add_url_rule('rbp', view_func=rbp_view, methods=['get'])
