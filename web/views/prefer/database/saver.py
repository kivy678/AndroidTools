# -*- coding:utf-8 -*-

##################################################################################################

from flask.views import MethodView
from flask import render_template

from web.views.prefer import view_db

from module.database import df_app

##################################################################################################


class DatabaseLoader(MethodView):
    def get(self):
        df_app.saveCSV()
        return "저장 완료"


save = DatabaseLoader.as_view('save')
view_db.add_url_rule('save', view_func=save)
