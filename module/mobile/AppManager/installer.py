# -*- coding:utf-8 -*-

###########################################################################################

from module.mobile.cmd import shell

from util.fsUtils import PathSplit
from util.Logger import LOG

from web.session import getSession

###########################################################################################

def cmdInstall(_path):
    LOG.info(f"{'[*]':<5}start install: " + PathSplit(_path)[1])

    cmd = f"adb install -r {_path}"
    shell.runCommand(cmd, shell=False)

    LOG.info(f"{'[*]':<5}Install End")

def cmdUninstall():
    pkg = getSession('pkg')
    LOG.info(f"{'[*]':<5}start uninstall: " + pkg)

    cmd = f"adb uninstall {pkg}"
    shell.runCommand(cmd, shell=False)

    LOG.info(f"{'[*]':<5}uninstall End")
