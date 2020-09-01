# -*- coding:utf-8 -*-

##########################################################################

from flask.views import MethodView
from flask import render_template, send_from_directory, request
from werkzeug.utils import secure_filename

from web.views.analysis import view_static

from util.fsUtils import Join, DirCheck, Delete

from common import getSharedPreferences
from webConfig import SHARED_PATH

##########################################################################

sp                  = getSharedPreferences(SHARED_PATH)
ANALYSIS_DIR        = sp.getString('ANALYSIS_DIR')

SPARK_DIR           = Join(ANALYSIS_DIR, 'spark')

##########################################################################

class Spark(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        Delete(SPARK_DIR)
        DirCheck(SPARK_DIR)

        return render_template(self.template_name)

    def post(self):
        f = request.files['LogFileName']
        fileName = f.filename

        f.save(Join(SPARK_DIR, secure_filename(fileName)))
        import module.spark.strace_filter

        return send_from_directory(directory=SPARK_DIR, filename='dump.csv', as_attachment=True)


spark = Spark.as_view('spark', template_name='analysis/static/spark.jinja')
view_static.add_url_rule('spark', view_func=spark, methods=['POST', 'get'])
