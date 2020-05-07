# -*- coding:utf-8 -*-

import argparse
from Dynamic.run import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Dynamic Mod', description='Android Setting')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 0.5')
    parser.add_argument('-i', '--ida', action='store_true',
                        help='IDA 디버깅 모드', dest='i')
    parser.add_argument('-j', '--jdb', action='store_true',
                        help='JDB 디버깅 모드', dest='j')

    args = parser.parse_args()

    if args is None:
        parser.print_help()
        exit()

    if args.i:
        idaStart()

    if args.j:
        jdbStart()

    print('Main done...')
