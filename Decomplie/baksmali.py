# -*- coding:utf-8 -*-

###########################################################################################

import os
import glob

from common import getSharedPreferences

from util.fsUtils import *
from util.Logger import LOG

from settings import *

from cmd import shell

###########################################################################################

BAKSMALI_TOOL       = Join(DECOMPLIE_PATH, "baksmali-2.1.3.jar")

IN_PATH             = Join(DECOM_WORK,     "in")
OUT_PATH            = Join(DECOM_WORK,     "out")
DECODE_PATH         = Join(DECOM_WORK,     "out", "decode")

DirCheck(IN_PATH)
DirCheck(OUT_PATH)

###########################################################################################



def runDecode(_file):
    sdir, fileName = PathSplit(_file)
    fdst = Join(IN_PATH, fileName)

    Copy(_file, fdst)

    LOG.info(f"{'[*]':<5}Start Decode: {fileName}")

    cmd = f"{BAKSMALI_TOOL} -o {DECODE_PATH} {fdst}"
    shell.runCommand(cmd, java=True)

    fName, _ = os.path.splitext(fileName)
    Copy(DECODE_PATH, Join(sdir, fName + '_smali'))

    LOG.info(f"{'[*]':<5}File Clean")
    Delete(IN_PATH)
    Delete(OUT_PATH)

    LOG.info(f"{'[*]':<5}End Decode")


def decodeBaksmali():
    sp = getSharedPreferences(SHARED_PATH)

    for _path in glob.glob(Join(sp.getString('WORKING_DIR'), '*')):
        if not isFile(_path):
            continue

        runDecode(_path)
