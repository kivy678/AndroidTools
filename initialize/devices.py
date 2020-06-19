# -*- coding:utf-8 -*-

################################################################################

import os
import shutil

import glob

from cmd.adb import DEVICE_DEBUG

from util.util import zipDecompress
from util.fsUtils import *

from settings import *

################################################################################


def cowExploit(adb):
	cmd = "adb push {0} /data/local/tmp".format(Join(PROP_PATH, 'mprop'))
	adb.runCommand(cmd, shell=False)

	cmd = "chmod 755 /data/local/tmp/mprop && /data/local/tmp/mprop ro.debuggable"
	adb.runCommand(cmd, shell=True)

	cmd = "getprop ro.debuggable"
	stdin = adb.runCommand(cmd, shell=True)

	return True if stdin == '1' else False
	

def appDecompress():
    for _path in glob.glob(Join(APP_PATH, '*')):
        _, app_name = PathSplit(_path)
        drc = Join(TMP_PATH, app_name)

        shutil.copy(_path, drc)
        path, _ = os.path.splitext(drc)
        zipDecompress(drc, path)

        yield path


def setDevice():
    adb = DEVICE_DEBUG.getPlatform()
    
    for decompress_dir in appDecompress():
        for _path in glob.glob(Join(decompress_dir, '*')):

            cmd = "adb install {0}".format(_path)
            adb.runCommand(cmd, shell=False)
	
    return cowExploit(adb)
