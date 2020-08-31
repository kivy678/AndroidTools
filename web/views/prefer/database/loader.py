# -*- coding:utf-8 -*-

##################################################################################################

from flask.views import MethodView
from flask import render_template, request

from web.views.prefer import view_db

from module.database import *

from web.session import setSession
from web.cache import setAnalisysCache

##################################################################################################


class DatabaseLoader(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        return render_template(self.template_name, enter=df_app.DATA_FRAME,
                                                   enter2=df_unity.DATA_FRAME,
                                                   enter3=df_il2cpp.DATA_FRAME)

    def post(self):

        pkg = request.form.get('pkg')
        fileName = request.form.get('fileName')
        sha256 = request.form.get('sha256')

        setAnalisysCache('analysis', {sha256: {'pkg': pkg, 'fileName': fileName}})

        setSession('pkg', pkg)
        setSession('fileName', fileName)

        return f"현재 분석중인 패키지명: {pkg}"


load = DatabaseLoader.as_view('load', template_name='prefer/database/load.jinja')
view_db.add_url_rule('load', view_func=load)
