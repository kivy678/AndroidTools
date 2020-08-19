# -*- coding:utf-8 -*-

from flask import Blueprint

view = Blueprint('analysis', __name__)
view_static = Blueprint('analysis.static', __name__)
view_dynamic = Blueprint('analysis.dynamic', __name__)


def setup(app):
    app.register_blueprint(view, url_prefix='/analysis/')
    app.register_blueprint(view_static, url_prefix='/analysis/static/')
    app.register_blueprint(view_dynamic, url_prefix='/analysis/dynamic/')


import web.views.analysis.index
import web.views.analysis.static.index
#import web.views.analysis.yara_engine
#import web.views.analysis.disasmbly
#import web.views.analysis.format
#import web.views.analysis.spark
