# -*- coding:utf-8 -*-

__all__=[
    'setApplicationInfor'
]

###########################################################################################

import glob

from module.mobile.Analysis.app import APP_INFOR

from util.Logger import LOG
from util.parser import *
from util.fsUtils import *
from util.hash import getSHA256

from webConfig import *

from module.mobile.cmd import shell

###########################################################################################

APK_TOOL 			= Join(DEBUG_PATH, "apktool_2.4.1.jar")

IN_PATH 			= Join(ANALYSIS_WORK, "in")
OUT_PATH 			= Join(ANALYSIS_WORK, "out")

###########################################################################################

def cleanFile():
    Delete(IN_PATH)
    Delete(OUT_PATH)


def readySample(_file) -> str: 			# DecodePath
    sdir, fileName = PathSplit(_file)
    fdst = Join(IN_PATH, fileName)

    Copy(_file, fdst)

    LOG.info(f"{'[*]':<5}start decode: {fileName}")
    DECODE_PATH = Join(OUT_PATH, fileName)

    cmd = f"{APK_TOOL} d -f -o {DECODE_PATH} {fdst}"
    shell.runCommand(cmd, java=True)

    return Join(OUT_PATH, fileName)


def setApplicationInfor(_path):
    cleanFile()
    app = APP_INFOR()

    app.decodePath = readySample(_path)
    app.sha256 = getSHA256(_path)

    MANIFEST = Join(app.decodePath, "AndroidManifest.xml")

    LOG.info(f"{'':>5}Start XML Parsing")
    app.parser(XmlParser(MANIFEST))

    LOG.info(f"{'':>5}Start JSON Parsing")
    app.parser(JsonParser(MANIFEST))

    LOG.info(f"{'[*]':<5}PackageName:{app.pkgName}")

    LOG.info(f"{'[*]':<5}File Clean")
    cleanFile()

    return True
