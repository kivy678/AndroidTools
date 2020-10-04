# -*- coding:utf-8 -*-

##########################################################################

import os

from flask.views import MethodView
from flask import render_template, request
from werkzeug.utils import secure_filename

from web.views.analysis import view_dynamic

from util.fsUtils import Join, DirCheck, Delete

from common import getSharedPreferences
from webConfig import SHARED_PATH, BASE_DIR

##########################################################################

sp              = getSharedPreferences(SHARED_PATH)
ANALYSIS_DIR    = sp.getString('ANALYSIS_DIR')

FRIDA_DIR       = Join(BASE_DIR, 'module', 'frida')
MERGE_DIR       = Join(FRIDA_DIR, 'js')

##########################################################################


class FRIDA(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name


    def get(self):
        os.chdir(MERGE_DIR)
        os.system('python merge')

        os.chdir(FRIDA_DIR)
        os.system(f'python ui.py')

        os.chdir(BASE_DIR)

        return "UI 실행완료"


frida_view = FRIDA.as_view('frida', template_name='')
view_dynamic.add_url_rule('frida', view_func=frida_view)
