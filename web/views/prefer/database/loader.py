# -*- coding:utf-8 -*-

##################################################################################################

from flask.views import MethodView
from flask import render_template, request
from flask import redirect

from web.views.prefer import view_db

from module.database import *

from web.session import setSession
from web.cache import setAnalisysCache
from web.cache import getCache

from common import getSharedPreferences
from webConfig import PROCESS_PATH

##################################################################################################

sp = getSharedPreferences(PROCESS_PATH)
ed = sp.edit()

##################################################################################################


class DatabaseLoader(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self, target=''):
        f = f'fetch_{target}'

        if hasattr(self, f) is False:
            return redirect('/prefer/index')

        return getattr(self, f)()


    def fetch_app(self):
        return render_template('prefer/database/load.jinja', enter=df_app.DATA_FRAME,
                                                   enter2=df_unity.DATA_FRAME,
                                                   enter3=df_il2cpp.DATA_FRAME)

    def fetch_dev(self):
        return render_template('prefer/database/load2.jinja', enter=df_lib.DATA_FRAME)

    def post(self):

        pkg = request.form.get('pkg')
        fileName = request.form.get('fileName')
        sha256 = request.form.get('sha256')

        setAnalisysCache('analysis', {sha256: {'pkg': pkg, 'fileName': fileName}})
        cmp_analysis = ', '.join([k for k in getCache('analysis')])

        setSession('pkg', pkg)
        setSession('fileName', fileName)

        ed.putString('pkg', pkg)
        ed.putString('fileName', fileName)
        ed.putString('sha256', sha256)
        ed.commit()

        return f"<pre>분석중인 패키지명:\t{pkg}\n비교 분석중인:\t{cmp_analysis}</pre>"


load = DatabaseLoader.as_view('load', template_name='')
view_db.add_url_rule('load/<string:target>', view_func=load)
