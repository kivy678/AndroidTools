# -*- coding:utf-8 -*-

from enum import Enum, unique, auto

@unique
class STATUS(Enum):
    INIT              = 'INIT'
    FILE_INIT         = 'FILE_INIT'
    ANALYSIS          = 'ANALYSIS'
    FAILED            = 'FAILED'


DEV_COLUMNS=[
    'model',
    'cpu',
    'su',
    'setup',
]

APP_COLUMNS=[
    'fileName',
    'pkg',
    'ctime',
    'status',
]
