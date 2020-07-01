# -*- coding:utf-8 -*-

#############################################################################

import os

from util.fsUtils import Delete, DirCheck

from settings import CACHE

#############################################################################

def clear():
    Delete(CACHE)
    DirCheck(CACHE)
