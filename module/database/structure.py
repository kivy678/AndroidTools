# -*- coding:utf-8 -*-

from enum import Enum, unique, auto

@unique
class STATUS(Enum):
    INIT              = 'INIT'


DEV_COLUMNS=[
    'model',
    'cpu',
    'su',
    'setup'
]

APP_COLUMNS=[
    'pkg'
]

