# -*- coding:utf-8 -*-

#############################################################################

import env

import os
import glob
import argparse

from util.fsUtils import *

from settings import *

from initialize.setdevice import setDevice
from initialize.base import AndroidBase
from initialize.initApp import setApplicationInfor

from util.Logger import LOG
from common import getSharedPreferences

from DebugMod.inject_debug import allInjection
from DebugMod.apk_install import installAllFile
from DebugMod.set_wait import getPackageName, setDebug

from Analysis.memdump import getMemoryDump

from Decomplie.baksmali import decodeBaksmali

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

    parser.add_argument('-I', '--install', action='store_true',
                        help='앱 설치', dest='I')

    parser.add_argument('-w', '--wait', action='store_true',
                        help='Waiting 모드 변환', dest='w')

    parser.add_argument('--decomplie', action='store_true',
                        help='디컴파일', dest='decomp')

    parser.add_argument('-a', '--analysis', action='store_true',
                        help='분석', dest='a')

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
        sp = getSharedPreferences(SHARED_PATH)

        for filePath in glob.glob(Join(sp.getString('WORKING_DIR'), '*')):
            setApplicationInfor(filePath)

    if args.decomp:
        decodeBaksmali()

    print('Main done...')
