# -*- coding:utf-8 -*-

###########################################################################################

from module.mobile.cmd import shell

from util.fsUtils import PathSplit
from util.Logger import LOG

###########################################################################################

def installer(_path):
    LOG.info(f"{'[*]':<5}start install: " + PathSplit(_path)[1])

    cmd = f"adb install -r {_path}"
    shell.runCommand(cmd, shell=False)

    LOG.info(f"{'[*]':<5}Install End")
