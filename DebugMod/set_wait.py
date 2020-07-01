# -*- coding:utf-8 -*-

__all__=[
    'getPackageName'
]

###########################################################################################

from mining.database import df

from util.Logger import LOG

from cmd import *

###########################################################################################


def setDebug(package, dbg=True):
    mode = "set" if dbg else "clear"
    option = "-w" if dbg else ""

    cmd = f"adb shell am {mode}-debug-app {option} {package}"
    LOG.info(f"{'[*]':<5}{mode} debug {package}")

    dev.runCommand(cmd, shell=True)


def getPackageName():
    for sha256 in df.DATA_FRAME.index.tolist():
        setDebug(df.DATA_FRAME.loc[sha256, 'pkg'])
