# -*- coding:utf-8 -*-

###########################################################################################

import glob
from bs4 import BeautifulSoup

from util.fsUtils import *
from util.Logger import LOG

from settings import *

from cmd import *

###########################################################################################

APK_TOOL            = Join(DEBUG_PATH,  "apktool_2.4.1.jar")

IN_PATH             = Join(DMOD_WORK,   "in")
OUT_PATH            = Join(DMOD_WORK,   "out")
DECODE_PATH         = Join(DMOD_WORK,   "out", "decode")

MANIFEST            = Join(DECODE_PATH, "AndroidManifest.xml")

DirCheck(IN_PATH)
DirCheck(OUT_PATH)

###########################################################################################

def setDebug(package, dbg=True):
    mode = "set" if dbg else "clear"
    option = "-w" if dbg else ""

    cmd = f"adb shell am {mode}-debug-app {option} {package}"
    LOG.info(f"{'[*]':<5}{mode} debug {package}")

    dev.runCommand(cmd, shell=True)


def readManifest():
    try:
        with open(MANIFEST) as fr:
            soup = BeautifulSoup(fr, "lxml-xml")
            return soup.manifest.get("package")

    except Exception as e:
        LOG.info(e)
        exit()


def decode(_file):
    sdir, fileName = PathSplit(_file)
    fdst = Join(IN_PATH, fileName)

    Copy(_file, fdst)

    try:
        LOG.info(f"{'[*]':<5}start decode: " + fileName)

        cmd = f"{APK_TOOL} d -f -o {DECODE_PATH} {fdst}"
        shell.runCommand(cmd, java=True)

        return readManifest()

    except Exception as e:
        LOG.info(e)
        return False

    finally:
        LOG.info(f"{'[*]':<5}File Clean")
        Delete(IN_PATH)
        Delete(OUT_PATH)


def getPackageName(dpath):
    PATH = Join(dpath, '*')

    for _path in glob.glob(PATH):
        if not isFile(_path):
            continue

        pkg = decode(_path)
        LOG.info(f"{'[*]':<5}getPackageName: {pkg}")
        yield (pkg)
