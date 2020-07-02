# -*- coding:utf-8 -*-

import env

import os

from Analysis.frida.run import *
from mining.database import df

if __name__ == '__main__':

    for sha256 in df.DATA_FRAME.index.tolist():
        Hook(df.DATA_FRAME.loc[sha256, 'pkg'])

    print('Main done...')
