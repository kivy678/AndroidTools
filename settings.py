# -*- coding:utf-8 -*-

#############################################################################

import os

#############################################################################

BASE_DIR 		= os.path.dirname(os.path.realpath(__file__))
LOGGER_PATH 	= os.path.join(BASE_DIR, "LOG")

VAR_PATH 		= os.path.join(BASE_DIR, "var")
TMP_PATH 		= os.path.join(BASE_DIR, "tmp")

SHARED_PATH 	= os.path.join('util', 'shared_prefs', 'setup.xml')

#############################################################################

APP_PATH 		= os.path.join(VAR_PATH, "app")
PROP_PATH 		= os.path.join(VAR_PATH, "prop")
SERVER_PATH 	= os.path.join(VAR_PATH, "server")
DEBUG_PATH 		= os.path.join(VAR_PATH, "debug")
DECOMPLIE_PATH 	= os.path.join(VAR_PATH, "decomplie")

#############################################################################

DMOD_PATH 		= os.path.join(BASE_DIR, "DebugMod")
DMOD_WORK 		= os.path.join(DMOD_PATH, "work")

#############################################################################

DECOM_PATH 		= os.path.join(BASE_DIR, "Decomplie")
DECOM_WORK 		= os.path.join(DECOM_PATH, "work")

#############################################################################