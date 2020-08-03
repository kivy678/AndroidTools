# -*- coding:utf-8 -*-

###########################################################################################

from mining.database import df
from Analysis import app

from util.Logger import LOG
from settings import DUMP_PATH

from Analysis.frida.dump.fridump3 import DUMP

###########################################################################################

def getMemoryDump():
    for sha256 in df.DATA_FRAME.index.tolist():
        app.pkgName = df.DATA_FRAME.loc[sha256, 'pkg']

        LOG.info(f"{'[*]':<5}START MEMORY DUMP")
        DUMP(DUMP_PATH, app.pkgName, strings=True, log=False)
        LOG.info(f"{'[*]':<5}END MEMORY DUMP")
