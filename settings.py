# -*- coding:utf-8 -*-

#############################################################################

import os
from util.fsUtils import Join

#############################################################################

BASE_DIR 		= os.path.dirname(os.path.realpath(__file__))
LOGGER_PATH 	= Join(BASE_DIR, "LOG")
LOG_PRINT 		= True

GLOBAL_SETTINGS = Join(BASE_DIR, "global.ini")

VAR_PATH 		= Join(BASE_DIR, "var")
TMP_PATH 		= Join(BASE_DIR, "tmp")

SHARED_PATH 	= Join('common', 'shared_prefs', 'setup.xml')

#############################################################################
############################### UTIL FILE ###################################

APP_PATH 		= Join(VAR_PATH, "app")
PROP_PATH 		= Join(VAR_PATH, "prop")
SERVER_PATH 	= Join(VAR_PATH, "server")
DEBUG_PATH 		= Join(VAR_PATH, "debug")
DECOMPLIE_PATH 	= Join(VAR_PATH, "decomplie")

#############################################################################
############################## PROJECT NAME #################################

DMOD_PATH 		= Join(BASE_DIR, "DebugMod")
DMOD_WORK 		= Join(DMOD_PATH, "work")

#############################################################################

DECOM_PATH 		= Join(BASE_DIR, "Decomplie")
DECOM_WORK 		= Join(DECOM_PATH, "work")

#############################################################################

ANALYSIS_PATH	= Join(BASE_DIR, "Analysis")
YARA_RULE 		= Join(ANALYSIS_PATH, "yara")
DUMP_PATH 		= r'c:\tmp\dump'

#############################################################################

CACHE 			= Join(BASE_DIR, 'mining', 'database', 'cache')
