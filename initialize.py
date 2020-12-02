# -*- coding:utf-8 -*-

##################################################################################################

__version__ = '1.3.1'

##################################################################################################

import platform

import argparse
import configparser

from common import getSharedPreferences
from util.fsUtils import *

from webConfig import *

##################################################################################################

for dirName in [LOGGER_PATH, SHARED_PATH_DIR, CACHE]:
    DirCheck(dirName)

##################################################################################################

sp                  = getSharedPreferences(SHARED_PATH)

config              = configparser.ConfigParser()
config.read(GLOBAL_SETTINGS)

WORKING_DIR         = config['WORK'].get('WORKING_DIR')
DATA_DIR            = config['WORK'].get('DATA_DIR')

SAMPLE_DIR          = Join(WORKING_DIR, 'sample')
DECODE_DIR          = Join(WORKING_DIR, 'decode')
ANALYSIS_DIR        = Join(WORKING_DIR, 'analysis')

TMP_DIR             = Join(WORKING_DIR, 'tmp')

##################################################################################################

system_os           = platform.system()
arch, _             = platform.architecture()

ed                  = sp.edit()
ed.putString("OS",    system_os )
ed.putString("ARCH",  f'x{arch[:2]}')
ed.commit()

##################################################################################################

JADX_PATH           = config['TOOL'].get('JADX')
JUST_DECOMPILE_PATH = config['TOOL'].get('JUST_DECOMPILE')
IL2CPP_DUMPER_PATH  = config['TOOL'].get('IL2CPP_DUMPER')
IDA_PATH            = config['TOOL'].get('IDA')

##################################################################################################

DYNAMORIO32         = config['TOOL-PC'].get('DYNAMORIO32')
DYNAMORIO64         = config['TOOL-PC'].get('DYNAMORIO64')
DRLTRACE32          = config['TOOL-PC'].get('DRLTRACE32')
DRLTRACE64          = config['TOOL-PC'].get('DRLTRACE64')

##################################################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Android Analysis', description='Android Analysis System')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {0}'.format(__version__))

    parser.add_argument('-i', '--init', action='store_true',
                        help='init', dest='i')

    parser.add_argument('-c', '--clear', action='store_true',
                        help='clear', dest='c')

    args = parser.parse_args()

    if args is None:
        parser.print_help()
        exit()

    if args.i:
        print("INIT SETTING")

        Delete(WORKING_DIR)
        Delete(DATA_DIR)
        for dirName in [DATA_DIR, SAMPLE_DIR, DECODE_DIR, ANALYSIS_DIR, TMP_DIR]:
            DirCheck(dirName)

        ed = sp.edit()
        ed.putString('WORKING_DIR', WORKING_DIR)
        ed.putString('DATA_DIR', DATA_DIR)

        ed.putString('SAMPLE_DIR', SAMPLE_DIR)
        ed.putString('DECODE_DIR', DECODE_DIR)
        ed.putString('ANALYSIS_DIR', ANALYSIS_DIR)
        ed.putString('TMP_DIR', TMP_DIR)

        ed.putString('JADX_PATH', JADX_PATH)
        ed.putString('JUST_DECOMPILE_PATH', JUST_DECOMPILE_PATH)
        ed.putString('IL2CPP_DUMPER_PATH', IL2CPP_DUMPER_PATH)
        ed.putString('IDA_PATH', IDA_PATH)

        ed.putBoolean('INIT_SETTING', True)
        ed.commit()

    if args.c:
        for dirName in [DECODE_DIR, ANALYSIS_DIR, TMP_DIR]:
            Delete(dirName)
            DirCheck(dirName)

    print("Main Done...")
