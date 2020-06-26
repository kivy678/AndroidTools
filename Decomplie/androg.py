# -*- coding:utf-8 -*-

import os

from cmd import dev

from util.fsUtils import *
from util.Logger import LOG

from settings import *


app_path = Join(TMP_PATH, 'test.apk')

cmd = f"androguard decompile -o tmp/out {app_path}"
dev.runCommand(cmd, shell=False)

LOG.info('Main done...')
