# -*- coding:utf-8 -*-

import os

from Frida.run import hook
from settings import BASE_DIR


if __name__ == '__main__':

    hook("owasp.mstg.uncrackable2")
    print('Main done...')
