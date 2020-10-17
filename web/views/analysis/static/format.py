# -*- coding:utf-8 -*-

##########################################################################

from flask.views import MethodView
from flask import render_template, request

from web.views.analysis import view_static

from util.fsUtils import Join, Walk, PathSplit, SplitExt

from common import getSharedPreferences
from webConfig import SHARED_PATH

from web.session import getSession

import elfformat

##########################################################################

sp 					= getSharedPreferences(SHARED_PATH)
DECODE_DIR			= sp.getString('DECODE_DIR')

##########################################################################

class FileFormat(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        data = list()
        analysis_path = Join(DECODE_DIR, getSession('fileName'), 'unzip')

        for _path in Walk(analysis_path):
            p = PathSplit(_path)[1]
            ext = SplitExt(p)[1]

            if ext == ".so":
                data.append(_path)

        data = map(lambda x: x.replace(analysis_path, '')[1:], data)

        return render_template(self.template_name, enter=data)

    def post(self):
        analysis_path = Join(DECODE_DIR, getSession('fileName'), 'unzip')
        lib_path = Join(analysis_path, request.form.get('lib'))
        f = request.form.get('format')

        try:
            if f in ['h', 'p', 's', 'd', 'S', 'dS', 'r', 'rp']:
                return "<pre>" + elfformat.parser(lib_path, f) + "<pre>"
            else:
                return "<pre>" + '\n'.join([i for i in elfformat.parser(lib_path, '')]) + "<pre>"

        except Exception as e:
            print(e)
            return "잘못된 형식의 파일입니다."


ft = FileFormat.as_view('format', template_name='analysis/static/format.jinja')
view_static.add_url_rule('format', view_func=ft)
