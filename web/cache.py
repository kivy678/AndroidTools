# -*- coding:utf-8 -*-

__all__=[
    'getCache',
    'setCache',
    'delCache'
]

##################################################################################################

from flask_caching import Cache

from webConfig import FLASK_SESSION, _REDIS_CACHE_CONFIG

from module.database.redisq import RedisQueue

##################################################################################################

simple_config = {
    "DEBUG": True,
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}

reids_config = {
    "DEBUG": True,
    "CACHE_TYPE": "redis",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_REDIS_HOST": _REDIS_CACHE_CONFIG['host'],
    "CACHE_REDIS_PORT": _REDIS_CACHE_CONFIG['port'],
    "CACHE_REDIS_DB": _REDIS_CACHE_CONFIG['db']
}

def getConfig():
    rq = RedisQueue()
    rq.connect(_REDIS_CACHE_CONFIG)

    if rq.conn:
        rq.close()
        return reids_config
    else:
        return simple_config

##################################################################################################

FlaskCache = Cache(config=getConfig())

def setup(app):
    FlaskCache.init_app(app)

##################################################################################################

def getCache(k):
    return FlaskCache.get(k)

def setCache(k, r, timeout=600):
    FlaskCache.set(k, r, timeout=timeout)

def delCache(k):
    FlaskCache.delete(k)

##################################################################################################
