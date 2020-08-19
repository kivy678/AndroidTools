# -*- coding:utf-8 -*-

from flask import Blueprint

view = Blueprint('app', __name__)


def setup(app):
    app.register_blueprint(view, url_prefix='/app/')


import web.views.app.index
import web.views.app.applist
import web.views.app.analysis
import web.views.app.installer
import web.views.app.debug
import web.views.app.wait
import web.views.app.decomplie
