# -*- coding:utf-8 -*-

from flask import Blueprint

view = Blueprint('decomplie', __name__)


def setup(app):
    app.register_blueprint(view, url_prefix='/decomplie/')


import web.views.decomplie.index
