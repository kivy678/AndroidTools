# -*- coding:utf-8 -*-

from flask import Blueprint

view            = Blueprint('pc', __name__)
view_dynamic    = Blueprint('pc.dynamic', __name__)


def setup(app):
    app.register_blueprint(view,         url_prefix='/pc/')
    app.register_blueprint(view_dynamic, url_prefix='/pc/dynamic/')

import web.views.pc.index
import web.views.pc.dynamic.dynamorio
