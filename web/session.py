# -*- coding:utf-8 -*-

__all__=[
    'getSession',
    'setSession',
    'popSession',
    'clearSession'
]

##################################################################################################

from datetime import timedelta

from flask import session, escape
from flask_session import Session

from webConfig import FLASK_SESSION, _REDIS_SESSION_CONFIG

from module.database.redisq import RedisQueue

##################################################################################################

rq = RedisQueue()
r_conn = rq.connect(_REDIS_SESSION_CONFIG)

sess = Session()

##################################################################################################

def setup(app):
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)
    app.config['SESSION_FILE_THRESHOLD'] = 10

    if r_conn:
        app.config['SESSION_TYPE'] = "redis"
        app.config['SESSION_REDIS'] = r_conn
    else:
        app.config['SESSION_TYPE'] = "filesystem"
        app.config['SESSION_FILE_DIR'] = FLASK_SESSION

    sess.init_app(app)

##################################################################################################

def getSession(k):
    return session.get(k, None)

def setSession(k, r):
    session[k] = r

def popSession(k):
    return session.pop(k, None)

def clearSession():
    session.clear()

##################################################################################################
