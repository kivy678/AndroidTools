# -*- coding:utf-8 -*-

from util.sharedpreference import SharedPreferences

def getSharedPreferences(fpath):
    return SharedPreferences(fpath)
