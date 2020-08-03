# -*- coding:utf-8 -*-

#############################################################################

import os
from util.fsUtils import Join

#############################################################################

BASE_DIR 		= os.path.dirname(os.path.realpath(__file__))

LOGGER_PATH 	= Join(BASE_DIR, "LOG")
LOG_PRINT 		= True

GLOBAL_SETTINGS = Join(BASE_DIR, "global.ini")
SHARED_PATH 	= Join('common', 'shared_prefs', 'setup.xml')

VAR_PATH 		= Join(BASE_DIR, "var")
TMP_PATH 		= Join(BASE_DIR, "tmp")

FLASK_SESSION	= Join(BASE_DIR, "__session__")

#############################################################################
############################### UTIL FILE ###################################

APP_PATH 		= Join(VAR_PATH, "app")
SERVER_PATH 	= Join(VAR_PATH, "server")
DEBUG_PATH 		= Join(VAR_PATH, "debug")
DECOMPLIE_PATH 	= Join(VAR_PATH, "decomplie")

#############################################################################
############################## PROJECT NAME #################################

SET_WORK 		= Join(TMP_PATH, "set")

#############################################################################

DMOD_PATH 		= Join(TMP_PATH, "DebugMod")
DMOD_WORK 		= Join(DMOD_PATH, "work")

#############################################################################

DECOM_PATH 		= Join(TMP_PATH, "Decomplie")
DECOM_WORK 		= Join(DECOM_PATH, "work")

#############################################################################

ANALYSIS_PATH	= Join(TMP_PATH, "Analysis")
ANALYSIS_WORK	= Join(ANALYSIS_PATH, "work")

YARA_RULE 		= Join(ANALYSIS_PATH, "yara")
DUMP_PATH 		= r'c:\tmp\dump'

#############################################################################

CACHE 			= Join(BASE_DIR, 'module', 'database', 'cache')

#############################################################################