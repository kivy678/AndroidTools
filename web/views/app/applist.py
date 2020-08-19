# -*- coding:utf-8 -*-

##########################################################################

import glob

from flask.views import MethodView
from flask import render_template, request
from flask import redirect, url_for

from web.views.app import view

from common import getSharedPreferences
from webConfig import SHARED_PATH

from util.fsUtils import Join, PathSplit

##########################################################################

sp = getSharedPreferences(SHARED_PATH)
SAMPLE_DIR = sp.getString('SAMPLE_DIR')

##########################################################################

class AppList(MethodView):
    def get(self, mode=''):
        f = f'fetch_mode'

        if False == hasattr(self, f):
            return redirect('/app/index')

        return getattr(self, f)(mode)

    def fetch_mode(self, mode):
        app_list = ( PathSplit(path)[1] for path in glob.glob(Join(SAMPLE_DIR, '*')))

        return render_template('app/list.jinja', enter=app_list, mode_url=f"/app/{mode}")


class AppDecomplie(MethodView):
    def get(self, mode=''):
        f = f'fetch_mode'

        if False == hasattr(self, f):
            return redirect('/app/index')

        return getattr(self, f)(mode)

    def fetch_mode(self, mode):
        app_list = ( PathSplit(path)[1] for path in glob.glob(Join(SAMPLE_DIR, '*')))

        return render_template('app/list.jinja', enter=app_list, mode_url=f"/app/decmp/{mode}")


app_list = AppList.as_view('list')
view.add_url_rule('list/<mode>', view_func=app_list)

app_decmp = AppDecomplie.as_view('decmp')
view.add_url_rule('decmp/<mode>', view_func=app_decmp)
