# -*- coding:utf-8 -*-

__all__ = [
    'getPackageName'
]

###########################################################################################

from mining.database import df

from util.Logger import LOG

from cmd import *

###########################################################################################


def setDebug(package, dbg=True):
    LOG.info(f"{'[*]':<5}Package Stop {package}")
    cmd = f"am force-stop {package}"
    dev.runCommand(cmd, shell=True)

    LOG.info(f"{'[*]':<5}Data Clear {package}")
    cmd = f"pm clear {package}"
    dev.runCommand(cmd, shell=True)

    mode = "set" if dbg else "clear"
    option = "-w" if dbg else ""

    cmd = f"am {mode}-debug-app {option} {package}"
    LOG.info(f"{'[*]':<5}{mode} debug {package}")

    dev.runCommand(cmd, shell=True)


def getPackageName(dbg=True):
    for sha256 in df.DATA_FRAME.index.tolist():
        setDebug(df.DATA_FRAME.loc[sha256, 'pkg'], dbg=dbg)
