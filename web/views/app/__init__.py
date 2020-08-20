# -*- coding:utf-8 -*-

from flask import Blueprint

view = Blueprint('app', __name__)


def setup(app):
    app.register_blueprint(view, url_prefix='/app/')


import web.views.app.index
import web.views.app.app
import web.views.app.wait
import web.views.app.decomplie
