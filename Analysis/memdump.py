# -*- coding:utf-8 -*-

###########################################################################################

from Analysis import app

from util.Logger import LOG
from settings import DUMP_PATH

from Analysis.frida.dump.fridump3 import DUMP

###########################################################################################

def getMemoryDump():
	
	LOG.info(f"{'[*]':<5}START MEMORY DUMP")
	DUMP(DUMP_PATH, app.pkgName, strings=True, log=False)
	LOG.info(f"{'[*]':<5}END MEMORY DUMP")
