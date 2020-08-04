# -*- coding:utf-8 -*-

##################################################################################################

from flask import Flask

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

##################################################################################################

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')


app.config.from_object('web.security')
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

##################################################################################################

from web.cache import setup as CacheSetup
from web.session import setup as SessionSetup
from web.worker import setup as WorkerSetup

CacheSetup(app)
SessionSetup(app)
WorkerSetup(app)

##################################################################################################

from web.views.base import setup as BaseSetup
from web.views.preferences import setup as PreferencesSetup
from web.views.device import setup as DevSetup
from web.views.decomplie import setup as DecomplieSetup
from web.views.analysis import setup as AnalysisSetup

BaseSetup(app)
DevSetup(app)
DecomplieSetup(app)
AnalysisSetup(app)
PreferencesSetup(app)

##################################################################################################

from web.init import setup as UserSetup

UserSetup()

##################################################################################################
