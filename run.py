# -*- coding:utf-8 -*-

import os

from DebugMod.inject_debug import injection
from settings import BASE_DIR

PATH = os.path.join(
    BASE_DIR, r'DebugMod\tmp\app-release.apk')

if __name__ == '__main__':

    injection(PATH)
    print('Main done...')
