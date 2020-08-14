# -*- coding:utf-8 -*-

##########################################################################

from flask.views import MethodView
from flask import render_template, request

from werkzeug.utils import secure_filename

from web.views.analysis import view

from util.fsUtils import Join
from webConfig import STORAGE_PATH

##########################################################################

class Spark(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        return render_template(self.template_name)

    def post(self):
        f = request.files['LogFileName']
        fileName = f.filename

        f.save(Join(STORAGE_PATH, secure_filename(fileName)))

        return "업로드 완료"

spark = Spark.as_view('spark', template_name='analysis/spark.jinja')
view.add_url_rule('spark', view_func=spark, methods=['POST', 'get'])
