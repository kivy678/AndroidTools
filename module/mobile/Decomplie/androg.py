# -*- coding:utf-8 -*-

###########################################################################################

import os

from module.mobile.cmd import shell

from util.fsUtils import *
from util.Logger import LOG

from webConfig import *

###########################################################################################

def runAndrogDecode(_file):
    LOG.info(f"{'[*]':<5}Start Decode: {_file}")

    cmd = f"androguard decompile -o {_file}_androg {_file}"
    shell.runCommand(cmd, shell=False)

    LOG.info(f"{'[*]':<5}End Decode")
