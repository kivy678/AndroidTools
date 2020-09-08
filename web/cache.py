# -*- coding:utf-8 -*-

__all__=[
    'getCache',
    'setCache',
    'delCache',
    'lpush',
    'rpop'
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
    r_conn = rq.connect(_REDIS_CACHE_CONFIG)

    try:
        if r_conn:
            return reids_config
        else:
            return simple_config
    finally:
        rq.close()

##################################################################################################

FlaskCache = Cache(config=getConfig())

def setup(app):
    FlaskCache.init_app(app)
    clearCache()

##################################################################################################

def getCache(k):
    return FlaskCache.get(k)

def setCache(k, r, timeout=600):
    FlaskCache.set(k, r, timeout=timeout)

def setAnalisysCache(k, r, timeout=600):
    if getCache(k):
        d = getCache(k)
        sha256 = list(r.keys())[0]

        try:
            d.pop(sha256)
        except KeyError:
            d.update(r)

        setCache(k, d)
    else:
        setCache(k, r)

def delCache(k):
    FlaskCache.delete(k)

def clearCache():
    FlaskCache.clear()

##################################################################################################

def lpush(k, r):
    rq = RedisQueue()
    rq.connect(_REDIS_CACHE_CONFIG)

    try:
        if rq.conn:
            return rq.conn.lpush(k, r)
    finally:
        rq.close()


def rpop(k):
    rq = RedisQueue()
    rq.connect(_REDIS_CACHE_CONFIG)

    try:
        if rq.conn:
            return rq.conn.rpop(k)
    finally:
        rq.close()

##################################################################################################
