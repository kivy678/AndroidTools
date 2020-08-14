# -*- coding:utf-8 -*-

from flask import Blueprint

view = Blueprint('analysis', __name__)


def setup(app):
    app.register_blueprint(view, url_prefix='/analysis/')


import web.views.analysis.index
import web.views.analysis.static
import web.views.analysis.yara_engine
import web.views.analysis.disasmbly
import web.views.analysis.format
import web.views.analysis.spark
