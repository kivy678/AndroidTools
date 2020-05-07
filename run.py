# -*- coding:utf-8 -*-

import env

import os
import argparse

from DebugMod.inject_debug import injectionAllFile
from DebugMod.set_wait import getPackageName, setDebug
from DebugMod.apk_install import installAllFile

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Android Mod', description='Android Setting')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 0.5')

    parser.add_argument('-d', '--debug', action='store_true',
                        help='디버깅 모드 변환', dest='d')
    parser.add_argument('-w', '--wait', action='store_true',
                        help='Waiting 모드 변환', dest='w')

    parser.add_argument('-I', '--install', action='store_true',
                        help='앱 설치', dest='I')

    args = parser.parse_args()

    if args is None:
        parser.print_help()
        exit()

    if args.d:
        injectionAllFile()

    if args.w:
        for i in getPackageName():
            setDebug(i[1], True)

    if args.I:
        installAllFile()

    print('Main done...')
