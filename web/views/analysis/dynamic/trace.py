# -*- coding:utf-8 -*-

##########################################################################

from flask.views import MethodView
from flask import render_template, request
from werkzeug.utils import secure_filename

from web.views.analysis import view_dynamic

from util.fsUtils import Join, DirCheck, Delete

from common import getSharedPreferences
from webConfig import SHARED_PATH

##########################################################################

sp                  = getSharedPreferences(SHARED_PATH)
ANALYSIS_DIR        = sp.getString('ANALYSIS_DIR')

ES_DIR              = Join(ANALYSIS_DIR, 'es')
DBG_BP              = {"ARM": "700020E1", "THUMB": "00BE", "X86": "CC"}
DBG_SIZE            = {"ARM": 4,          "THUMB": 2,      "X86": 1}

##########################################################################


class TRACE(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name


    def get(self):
        return render_template(self.template_name)


    def post(self):
        f = request.files['LogFileName']
        fileName = f.filename

        csv_path = Join(ES_DIR, secure_filename(fileName))
        f.save(csv_path)

        platform = request.form.get("platform")
        baseAddr = request.form.get("GetBase")



        return "BP 완료"


st_view = TRACE.as_view('trace', template_name='analysis/dynamic/strace.jinja')
view_dynamic.add_url_rule('trace', view_func=st_view, methods=['POST', 'get'])
