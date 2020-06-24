# -*- coding:utf-8 -*-

import env
import os

from cmd import dev

from settings import *

app_path = os.path.join(TMP_PATH, 'test.apk')

cmd = f"androguard decompile -o tmp/out {app_path}"
dev.runCommand(cmd, shell=False)

print('Main done...')
