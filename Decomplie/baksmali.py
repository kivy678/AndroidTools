# -*- coding:utf-8 -*-

###########################################################################################

import os
import glob

from util.fsUtils import *
from settings import *

from cmd import shell

###########################################################################################

BAKSMALI_TOOL       = os.path.join(DECOMPLIE_PATH,  "baksmali-2.1.3.jar")

IN_PATH             = os.path.join(DECOM_WORK,   "in")
OUT_PATH            = os.path.join(DECOM_WORK,   "out")
DECODE_PATH         = os.path.join(DECOM_WORK,   "out", "decode")

DirCheck(IN_PATH)
DirCheck(OUT_PATH)

###########################################################################################

def runDecode(_file):
    sdir, fileName = os.path.split(_file)
    fdst = os.path.join(IN_PATH, fileName)

    Copy(_file, fdst)

    print(f"{'[*]':<5}Start Decode: {fileName}")

    cmd = f"{BAKSMALI_TOOL} -o {DECODE_PATH} {fdst}"
    shell.runCommand(cmd, java=True)

    fName, _ = os.path.splitext(fileName)
    Copy(DECODE_PATH, os.path.join(sdir, fName + '_smali'))

    print(f"{'[*]':<5}File Clean")
    Delete(IN_PATH)
    Delete(OUT_PATH)

    print(f"{'[*]':<5}End Decode")


def allDecode(dpath):
    PATH = os.path.join(dpath, '*')

    for _path in glob.glob(PATH):
        if not os.path.isfile(_path):
            continue

        runDecode(_path)
