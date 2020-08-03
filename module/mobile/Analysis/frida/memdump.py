# -*- coding:utf-8 -*-

###########################################################################################

from module.mobile.Analysis.frida.dump.fridump3 import DUMP

from util.Logger import LOG
from webConfig import DUMP_PATH

###########################################################################################

def getMemoryDump(pkgName):
    LOG.info(f"{'[*]':<5}START MEMORY DUMP")
    DUMP(DUMP_PATH, pkgName, strings=True, log=False)
    LOG.info(f"{'[*]':<5}END MEMORY DUMP")
