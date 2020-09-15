# -*- coding:utf-8 -*-

##########################################################################

from module.frida.dump.fridump3 import DUMP

from util.fsUtils import Join, DirCheck, Delete
from util.Logger import LOG

from common import getSharedPreferences
from webConfig import SHARED_PATH

##########################################################################

sp                  = getSharedPreferences(SHARED_PATH)
ANALYSIS_DIR        = sp.getString('ANALYSIS_DIR')

##########################################################################

def getMemoryDump(pkg):
    dump_path = Join(ANALYSIS_DIR, 'MEMORY', pkg)
    Delete(dump_path)
    DirCheck(dump_path)

    LOG.info(f"{'[*]':<5}START MEMORY DUMP")
    DUMP(dump_path, pkg, strings=True, log=False)
    LOG.info(f"{'[*]':<5}END MEMORY DUMP")
