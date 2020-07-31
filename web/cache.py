# -*- coding:utf-8 -*-

##################################################################################################

from flask_caching import Cache

##################################################################################################

config = {
    "DEBUG": True,
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}

FlaskCache = Cache(config=config)

##################################################################################################

def setup(app):
    FlaskCache.init_app(app)

##################################################################################################

def getCache(k):
    return FlaskCache.get(k)

def setCache(k, r, timeout=600):
    FlaskCache.set(k, r, timeout=timeout)
    return None

def delCache(k):
    FlaskCache.delete(k)
    return None

##################################################################################################
