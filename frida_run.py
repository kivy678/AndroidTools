# -*- coding:utf-8 -*-

#############################################################################

import env

import os
import argparse

from module.mobile.Analysis.frida.local_run import *

#############################################################################

__version__ = '0.5.2'

#############################################################################

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='Android Frida', description='Frida Running')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {0}'.format(__version__))

    parser.add_argument('--hook', action='store_true',
                        help='Hook', dest='h')

    parser.add_argument('-a', '--attach', action='store_true',
                        help='Attach', dest='a')

    args = parser.parse_args()

    if args is None:
        parser.print_help()
        exit()

    if args.h:
        Hook("dz.angie.clean.master")

    if args.a:
        attachHook("dz.angie.clean.master")

    print('Main done...')
