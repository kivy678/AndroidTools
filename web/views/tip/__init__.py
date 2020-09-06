# -*- coding:utf-8 -*-

from flask import Blueprint

view = Blueprint('tip', __name__)


def setup(app):
    app.register_blueprint(view, url_prefix='/tip/')


import web.views.tip.index
import web.views.tip.opcode
