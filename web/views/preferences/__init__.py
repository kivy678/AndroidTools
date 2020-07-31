# -*- coding:utf-8 -*-

from flask import Blueprint

view = Blueprint('set', __name__)


def setup(app):
    app.register_blueprint(view, url_prefix='/set/')


import web.views.preferences.setting
