# -*- coding:utf-8 -*-

##########################################################################

import os

from flask.views import MethodView
from flask import render_template, request
from werkzeug.utils import secure_filename

from web.views.analysis import view_dynamic

from util.fsUtils import *

from common import getSharedPreferences
from webConfig import SHARED_PATH, BASE_DIR

##########################################################################

sp              = getSharedPreferences(SHARED_PATH)
ANALYSIS_DIR    = sp.getString('ANALYSIS_DIR')

MERGE_DIR       = Join(BASE_DIR, 'module', 'frida', 'js')

##########################################################################


class FRIDA(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name


    def get(self):
        js_list = [BaseName(i) for i in Walk(MERGE_DIR)
                    if BaseName(i).endswith('js') and not BaseName(i).startswith('merge')]

        js_list = self.changeNumber(js_list, '100')

        return render_template(self.template_name, enter=js_list)


    def post(self):
        self.changeNumber(request.form.getlist("checkScript"), '1')

        os.chdir(MERGE_DIR)
        os.system('python merge')
        os.chdir(BASE_DIR)

        os.system(f'python -m module.frida.ui.py')

        return "UI 실행 완료"


    def changeNumber(self, l, number):
        os.chdir(MERGE_DIR)

        _new = list()
        for scriptName in l:
            changeName = scriptName.split('-')
            changeName[1] = number
            os.rename(scriptName, '-'.join(changeName))
            _new.append('-'.join(changeName))

        os.chdir(BASE_DIR)

        return _new


frida_view = FRIDA.as_view('frida', template_name='analysis/dynamic/frida.jinja')
view_dynamic.add_url_rule('frida', view_func=frida_view)
