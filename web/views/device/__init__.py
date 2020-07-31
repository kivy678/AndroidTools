# -*- coding:utf-8 -*-

from flask import Blueprint

view = Blueprint('dev', __name__)


def setup(app):
    app.register_blueprint(view, url_prefix='/dev/')


import web.views.device.list
import web.views.device.work
