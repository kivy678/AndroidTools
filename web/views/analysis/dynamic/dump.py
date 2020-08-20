# -*- coding:utf-8 -*-

################################################################################

from flask.views import MethodView
from flask import render_template, request
from flask import redirect, url_for

from web.views.analysis import view_dynamic
from module.mobile.Analysis.dynamic.trace import straceStart
from module.mobile.Analysis.dynamic.memdump import getMemoryDump

from web.session import getSession

################################################################################

class DumpMode(MethodView):
    def get(self, mode=''):
        f = f'fetch_{mode}'

        if False == hasattr(self, f):
            return redirect('/app/index')

        pkg = getSession('pkg')
        return getattr(self, f)(pkg)


    def fetch_strace(self, pkg):
        straceStart(pkg)
        return "Strace 덤프 완료"


    def fetch_memory(self, pkg):
        getMemoryDump(pkg)
        return "메모리 덤프 완료"


dump = DumpMode.as_view('dump')
view_dynamic.add_url_rule('dump/<mode>', view_func=dump)
