# -*- coding:utf-8 -*-

#############################################################################

import env

import os
import argparse

from settings import *

from initialize import setDevice
from initialize.base import AndroidBase
from initialize.initApp import setApplicationInfor

from util.Logger import LOG
from common import getSharedPreferences

from DebugMod.inject_debug import allInjection
from DebugMod.apk_install import installAllFile
from DebugMod.set_wait import getPackageName, setDebug

from Analysis.memdump import getMemoryDump

#############################################################################

__version__ = '0.5.1'

#############################################################################

#setDevice()
#AndroidBase()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='Android Analysis', description='Android Setting')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {0}'.format(__version__))

    parser.add_argument('-d', '--debug', action='store_true',
                        help='디버깅 모드 변환', dest='d')

    parser.add_argument('-I', '--install', action='store_true',
                        help='앱 설치', dest='I')

    parser.add_argument('-w', '--wait', action='store_true',
                        help='Waiting 모드 변환', dest='w')

    parser.add_argument('-a', '--analysis', help='분석', dest='a')

    args = parser.parse_args()

    if args is None:
        parser.print_help()
        exit()

    if args.d:
        allInjection(cpath)

    if args.w:
        for pkg in getPackageName(spath):
            setDebug(pkg, True)

    if args.I:
        installAllFile(ipath)

    if args.a:
        setApplicationInfor(args.a)
        #getMemoryDump()

    print('Main done...')
