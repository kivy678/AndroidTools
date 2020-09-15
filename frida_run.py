# -*- coding:utf-8 -*-

#############################################################################

import env

import os
import argparse

from module.frida.local_run import *

#############################################################################

__version__ = '0.5.2'

#############################################################################

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='Android Frida', description='Frida Running')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {0}'.format(__version__))

    parser.add_argument('-a', '--attach',
                        help='Attach', dest='a')

    args = parser.parse_args()

    if args is None:
        parser.print_help()
        exit()

    if args.a:
        attachHook(args.a)

    print('Main done...')
