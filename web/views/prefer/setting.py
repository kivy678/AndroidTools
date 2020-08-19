# -*- coding:utf-8 -*-

##################################################################################################

from flask.views import MethodView
from flask import render_template

from web.views.prefer import view

from common import getSharedPreferences
from webConfig import SHARED_PATH

##################################################################################################


class SetupPage(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        sp = getSharedPreferences(SHARED_PATH)
        sp.getString('WORKING_DIR')

        return f"작업 디렉토리: {sp.getString('WORKING_DIR')}"


setup_page = SetupPage.as_view('set', template_name='')
view.add_url_rule('set', view_func=setup_page)
