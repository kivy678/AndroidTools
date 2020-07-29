# -*- coding:utf-8 -*-

__all__=[
    'allInjection'
]

###########################################################################################

import os
import glob
from bs4 import BeautifulSoup

from util.fsUtils import *
from util.Logger import LOG

from settings import *

from cmd import *

###########################################################################################

APK_TOOL            = Join(DEBUG_PATH,  "apktool_2.4.1.jar")

SIGNAPK_TOOL        = Join(DEBUG_PATH,  "signapk", "signapk.jar")
CERTIFICATE_TOOL    = Join(DEBUG_PATH,  "signapk", "certificate.pem")
PK8_TOOL            = Join(DEBUG_PATH,  "signapk", "key.pk8")

IN_PATH             = Join(DMOD_WORK,   "in")
OUT_PATH            = Join(DMOD_WORK,   "out")
DECODE_PATH         = Join(DMOD_WORK,   "out", "decode")

MANIFEST            = Join(DECODE_PATH, "AndroidManifest.xml")
MANIFEST_WRITE      = Join(DECODE_PATH, "AndroidManifest_tmp.xml")

OUT_APK             = Join(OUT_PATH,    "out.apk")
KEY_APK             = Join(OUT_PATH,    "signed.apk")

DirCheck(IN_PATH)
DirCheck(OUT_PATH)

###########################################################################################

def cleanDir():
    Delete(IN_PATH)
    Delete(OUT_PATH)


def readManifest():
    try:
        with open(MANIFEST, "r", encoding='utf-8') as fr:
            soup = BeautifulSoup(fr, "lxml-xml")
            soup.application['android:debuggable'] = 'true'

            with open(MANIFEST_WRITE, "w", encoding='utf-8') as fw:
                fw.write(str(soup))
    except Exception as e:
        LOG.info(e)
        exit()


def fileManger():
    try:
        os.remove(MANIFEST)
        os.rename(MANIFEST_WRITE, MANIFEST)
    except Exception as e:
        LOG.info(e)
        return False


def injection(_file):
    sdir, fileName = PathSplit(_file)
    fdst = Join(IN_PATH, fileName)

    Copy(_file, fdst)

    LOG.info(f"{'[*]':<5}start decode: {fileName}")

    cmd = f"{APK_TOOL} d -f  -o {DECODE_PATH} {fdst}"
    shell.runCommand(cmd, java=True)

    #readManifest()
    #fileManger()

    LOG.info(f"{'[*]':<5}start build")
    cmd = f"{APK_TOOL} b -f -d -o {OUT_APK} {DECODE_PATH}"
    shell.runCommand(cmd, java=True)

    LOG.info(f"{'[*]':<5}sign code")
    cmd = f"{SIGNAPK_TOOL} {CERTIFICATE_TOOL} {PK8_TOOL} {OUT_APK} {KEY_APK}"
    shell.runCommand(cmd, java=True)

    f, ext = os.path.splitext(fileName)
    dpath = Join(sdir, f +'_signed.apk')
    Copy(KEY_APK, dpath)

    LOG.info(f"{'[*]':<5}File Clean")
    #cleanDir()

    LOG.info(f"{'[*]':<5}injection End")


def allInjection(dpath):
    PATH = Join(dpath, '*')

    for _path in glob.glob(PATH):
        if not isFile(_path):
            continue

        injection(_path)
