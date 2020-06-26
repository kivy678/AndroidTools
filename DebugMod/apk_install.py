# -*- coding:utf-8 -*-

###########################################################################################

import glob

from cmd import dev

from util.fsUtils import *
from util.Logger import LOG

###########################################################################################

def installer(_path):
    LOG.info(f"{'[*]':<5}start install: " + PathSplit(_path)[1])

    cmd = f"adb install -r {_path}"
    dev.runCommand(cmd, shell=False)

    LOG.info(f"{'[*]':<5}Install End")


def installAllFile(dpath):
    PATH = Join(dpath, '*')

    for fileName in glob.glob(PATH):
        if not isFile(fileName):
            continue

        installer(fileName)
