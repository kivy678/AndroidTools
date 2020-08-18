# -*- coding:utf-8 -*-

##################################################################################################

import argparse
import configparser

from common import getSharedPreferences
from util.fsUtils import *

from webConfig import *

##################################################################################################

config = configparser.ConfigParser()
config.read(GLOBAL_SETTINGS)

WORKING_DIR     = config['WORK'].get('working_dir')

SAMPLE_DIR      = Join(WORKING_DIR, 'sample')
DECODE_DIR      = Join(WORKING_DIR, 'decode')
ANALYSIS_DIR    = Join(WORKING_DIR, 'analysis')

TMP_DIR         = Join(WORKING_DIR, 'tmp')

##################################################################################################

__version__ = '0.13.0'

##################################################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Android Analysis', description='Android Analysis System')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {0}'.format(__version__))

    parser.add_argument('-i', '--init', action='store_true',
                        help='init', dest='i')

    args = parser.parse_args()

    if args is None:
        parser.print_help()
        exit()

    if args.i:
        sp = getSharedPreferences(SHARED_PATH)

        print("INIT SETTING")

        Delete(WORKING_DIR)
        for dirName in [SAMPLE_DIR, DECODE_DIR, ANALYSIS_DIR, TMP_DIR]:
            DirCheck(dirName)

        ed = sp.edit()
        ed.putString('WORKING_DIR', WORKING_DIR)
        ed.putString('SAMPLE_DIR', SAMPLE_DIR)
        ed.putString('DECODE_DIR', DECODE_DIR)
        ed.putString('ANALYSIS_DIR', ANALYSIS_DIR)
        ed.putString('TMP_DIR', TMP_DIR)

        ed.putBoolean('INIT_SETTING', True)
        ed.commit()

    print("Main Done...")
