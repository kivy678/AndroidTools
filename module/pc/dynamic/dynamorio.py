# -*- coding: utf-8 -*-

##################################################################################################

from module.mobile.cmd import shell

from common import getSharedPreferences
from webConfig import SHARED_PATH

from util.fsUtils import *
from util.Logger import LOG

##################################################################################################

sp                    = getSharedPreferences(SHARED_PATH)
ARCH                  = sp.getString('ARCH')

if ARCH == "x32":
    DYNAMORIO         = sp.getString('DYNAMORIO32')
    DRLTRACE          = sp.getString('DRLTRACE32')
elif ARCH == "x64":
    DYNAMORIO         = sp.getString('DYNAMORIO64')
    DRLTRACE          = sp.getString('DRLTRACE64')

##################################################################################################

def runDyanmorio(cmd, app):
    LOG.info(f"{'[*]':<5}start dynamorio: {cmd} {app}")
    run = "{DYNAMORIO} -c {cmd} -- {app}"
    #shell.runCommand(run, shell=False, timeout=600)
