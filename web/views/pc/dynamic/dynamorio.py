# -*- coding:utf-8 -*-

##########################################################################

from flask.views import MethodView
from flask import render_template, request
from flask import redirect, url_for

from web.views.pc import view_dynamic

from module.pc.dynamic.dynamorio import runDyanmorio

##########################################################################

##########################################################################


class Dynamorio(MethodView):
    def get(self, mode=''):
        f = f'fetch_{mode}'

        if hasattr(self, f) is False:
            return redirect('/pc/index')

        return getattr(self, f)()

    def fetch_debug(self):
        return "debug LV4"

    def fetch_instrace(self):
        return "instrace"

    def fetch_instrcalls(self):
        return "instrcalls"

    def fetch_drcov(self):
        return "drcov"

    def fetch_drltrace(self):
        return "drltrace"


dy = Dynamorio.as_view('dynamorio')
view_dynamic.add_url_rule('dynamorio/<mode>', view_func=dy)
