# -*- coding:utf-8 -*-

###########################################################################################

from Analysis import app

from util.Logger import LOG
from util.parser import *
from util.fsUtils import *

from settings import *

from cmd import *

###########################################################################################

APK_TOOL            = Join(DEBUG_PATH,  "apktool_2.4.1.jar")

IN_PATH             = Join(TMP_PATH,   "in")
OUT_PATH            = Join(TMP_PATH,   "out")
DECODE_PATH         = Join(TMP_PATH,   "out", "decode")

MANIFEST            = Join(DECODE_PATH, "AndroidManifest.xml")

DirCheck(IN_PATH)
DirCheck(OUT_PATH)

###########################################################################################


def cleanFile():
	Delete(IN_PATH)
	Delete(OUT_PATH)

	return True

def readySample(_file):
    sdir, fileName = PathSplit(_file)
    fdst = Join(IN_PATH, fileName)

    Copy(_file, fdst)

    LOG.info(f"{'[*]':<5}start decode: {fileName}")

    cmd = f"{APK_TOOL} d -f -o {DECODE_PATH} {fdst}"
    shell.runCommand(cmd, java=True)

    return True


def setApplicationInfor(_path):
	readySample(_path)
	LOG.info(f"{'':>5}Start XML Parsing")
	app.parser(XmlParser(MANIFEST))

	LOG.info(f"{'':>5}Start JSON Parsing")
	app.parser(JsonParser(MANIFEST))

	LOG.info(f"{'[*]':<5}PackageName:{app.pkgName}")

	LOG.info(f"{'[*]':<5}File Clean")
	cleanFile()

	return True
