# -*- coding:utf-8 -*-

import os

from DebugMod.inject_debug import injection
from settings import BASE_DIR

PATH = os.path.join(
    BASE_DIR, r'DebugMod\tmp\99B18C6A0072EB97801B630DA5E44BF7.apk')

if __name__ == '__main__':

    injection(PATH)
    print('done...')
