# -*- coding:utf-8 -*-

from flask import Blueprint

view = Blueprint('prefer', __name__)
view_db = Blueprint('prefer.database', __name__)


def setup(app):
    app.register_blueprint(view, url_prefix='/prefer/')
    app.register_blueprint(view_db, url_prefix='/prefer/database/')


import web.views.prefer.index
import web.views.prefer.setting

import web.views.prefer.database.index
import web.views.prefer.database.loader
