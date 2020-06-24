# -*- coding:utf-8 -*-

###########################################################################################

import os
import glob
from bs4 import BeautifulSoup

from util.fsUtils import *
from settings import *

from cmd import *

###########################################################################################

APK_TOOL            = os.path.join(DEBUG_PATH,  "apktool_2.4.1.jar")

SIGNAPK_TOOL        = os.path.join(DEBUG_PATH,  "signapk", "signapk.jar")
CERTIFICATE_TOOL    = os.path.join(DEBUG_PATH,  "signapk", "certificate.pem")
PK8_TOOL            = os.path.join(DEBUG_PATH,  "signapk", "key.pk8")

IN_PATH             = os.path.join(DMOD_WORK,   "in")
OUT_PATH            = os.path.join(DMOD_WORK,   "out")
DECODE_PATH         = os.path.join(DMOD_WORK,   "out", "decode")

MANIFEST            = os.path.join(DECODE_PATH, "AndroidManifest.xml")
MANIFEST_WRITE      = os.path.join(DECODE_PATH, "AndroidManifest_tmp.xml")

OUT_APK             = os.path.join(OUT_PATH,    "out.apk")
KEY_APK             = os.path.join(OUT_PATH,    "signed.apk")

DirCheck(IN_PATH)
DirCheck(OUT_PATH)

###########################################################################################

def readManifest():
    try:
        with open(MANIFEST) as fr:
            soup = BeautifulSoup(fr, "lxml-xml")
            soup.application['android:debuggable'] = 'true'

            with open(MANIFEST_WRITE, "w", encoding='utf-8') as fw:
                fw.write(str(soup))
    except Exception as e:
        print(e)
        exit()


def fileManger():
    try:
        os.remove(MANIFEST)
        os.rename(MANIFEST_WRITE, MANIFEST)
    except Exception as e:
        print(e)
        return False


def injection(_file):
    sdir, fileName = os.path.split(_file)
    fdst = os.path.join(IN_PATH, fileName)

    Copy(_file, fdst)

    print(f"{'[*]':<5}start decode: {fileName}")

    cmd = f"{APK_TOOL} d -f -o {DECODE_PATH} {fdst}"
    shell.runCommand(cmd, java=True)

    readManifest()
    fileManger()

    print(f"{'[*]':<5}start build")
    cmd = f"{APK_TOOL} b -f -o {OUT_APK} {DECODE_PATH}"
    shell.runCommand(cmd, java=True)

    print(f"{'[*]':<5}sign code")
    cmd = f"{SIGNAPK_TOOL} {CERTIFICATE_TOOL} {PK8_TOOL} {OUT_APK} {KEY_APK}"
    shell.runCommand(cmd, java=True)

    f, ext = os.path.splitext(fileName)
    dpath = os.path.join(sdir, f +'_signed.apk')
    Copy(KEY_APK, dpath)

    print(f"{'[*]':<5}File Clean")
    Delete(IN_PATH)
    Delete(OUT_PATH)

    print(f"{'[*]':<5}injection End")


def allInjection(dpath):
    PATH = os.path.join(dpath, '*')

    for _path in glob.glob(PATH):
        if not os.path.isfile(_path):
            continue

        injection(_path)
