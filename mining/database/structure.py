# -*- coding:utf-8 -*-

from enum import Enum, unique, auto

@unique
class STATUS(Enum):
    INIT              = 'INIT'


COLUMNS = [
    'positives',
    'type',
    'virobot',
    'rep',
    'rep_type',
    'status',
]
