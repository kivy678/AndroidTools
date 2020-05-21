# -*- coding:utf-8 -*-

#############################################################################
import os

#############################################################################
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
UTIL = os.path.join(BASE_DIR, "util")
TMP = os.path.join(BASE_DIR, "tmp")

IN = os.path.join(TMP, r"in\classes.dex")
OUT = os.path.join(TMP, "decode")

#############################################################################
BACK_TOOL = os.path.join(UTIL, "baksmali-2.1.3.jar")
