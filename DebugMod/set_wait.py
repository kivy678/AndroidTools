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

IN_PATH             = os.path.join(DMOD_WORK,   "in")
OUT_PATH            = os.path.join(DMOD_WORK,   "out")
DECODE_PATH         = os.path.join(DMOD_WORK,   "out", "decode")

MANIFEST            = os.path.join(DECODE_PATH, "AndroidManifest.xml")

DirCheck(IN_PATH)
DirCheck(OUT_PATH)

###########################################################################################

def setDebug(package, dbg=True):
    mode = "set" if dbg else "clear"
    option = "-w" if dbg else ""

    cmd = f"adb shell am {mode}-debug-app {option} {package}"
    print(f"{'[*]':<5}{mode} debug {package}")

    dev.runCommand(cmd, shell=True)


def readManifest():
    try:
        with open(MANIFEST) as fr:
            soup = BeautifulSoup(fr, "lxml-xml")
            return soup.manifest.get("package")

    except Exception as e:
        print(e)
        exit()


def decode(_file):
    sdir, fileName = os.path.split(_file)
    fdst = os.path.join(IN_PATH, fileName)

    Copy(_file, fdst)

    try:
        print(f"{'[*]':<5}start decode: " + fileName)

        cmd = f"{APK_TOOL} d -f -o {DECODE_PATH} {fdst}"
        shell.runCommand(cmd, java=True)

        return readManifest()

    except Exception as e:
        print(e)
        return False

    finally:
        print(f"{'[*]':<5}File Clean")
        Delete(IN_PATH)
        Delete(OUT_PATH)


def getPackageName(dpath):
    PATH = os.path.join(dpath, '*')

    for _path in glob.glob(PATH):
        if not os.path.isfile(_path):
            continue

        pkg = decode(_path)
        print(f"{'[*]':<5}getPackageName: {pkg}")
        yield (pkg)
