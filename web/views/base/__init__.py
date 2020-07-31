# -*- coding:utf-8 -*-

from flask import Blueprint

view = Blueprint('/', __name__)


def setup(app):
    app.register_blueprint(view, url_prefix='/')


import web.views.base.index
