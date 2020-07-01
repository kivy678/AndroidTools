# -*- coding:utf-8 -*-

#############################################################################

import env

import os
import glob
import argparse

from settings import *

from util.fsUtils import *
from util.Logger import LOG

from initialize.setdevice import setDevice
from initialize.base import AndroidBase
from initialize.initApp import allSetApplicationInfor

from common import getSharedPreferences

from DebugMod.inject_debug import allInjection
from DebugMod.set_wait import getPackageName, setDebug

from Analysis.memdump import getMemoryDump
from Analysis.debug.jdb.jdb import jdbStart

from Decomplie.baksmali import decodeBaksmali

from clear import clear

#############################################################################

__version__ = '0.5.2'

#############################################################################

AndroidBase()
setDevice()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='Android Analysis', description='Android Setting')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {0}'.format(__version__))

    parser.add_argument('-d', '--debug', action='store_true',
                        help='디버깅 모드 변환', dest='d')

    parser.add_argument('-w', '--wait', action='store_true',
                        help='Waiting 모드 변환', dest='w')

    parser.add_argument('--dynamic', action='store_true',
                        help='Waiting 모드 변환', dest='dynamic')

    parser.add_argument('--decomplie', action='store_true',
                        help='디컴파일', dest='decomp')

    parser.add_argument('-a', '--analysis', action='store_true',
                        help='분석', dest='a')

    parser.add_argument('--clear', action='store_true',
                        help='캐쉬클리어', dest='c')

    args = parser.parse_args()

    if args is None:
        parser.print_help()
        exit()

    if args.d:
        sp = getSharedPreferences(SHARED_PATH)
        allInjection(sp.getString('WORKING_DIR'))

    if args.dynamic:
        jdbStart()

    if args.w:
        getPackageName()

    if args.a:
        sp = getSharedPreferences(SHARED_PATH)
        allSetApplicationInfor(sp.getString('WORKING_DIR'))

    if args.decomp:
        decodeBaksmali()

    if args.c:
        clear()

    print('Main done...')
