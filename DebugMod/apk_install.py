# -*- coding:utf-8 -*-

import os
import glob

import shlex
import subprocess

from .settings import *


def installer(_file):
    print("[*] start install: " + os.path.split(_file)[1])
    cmd = f"adb install -r {_file}"
    subprocess.call(shlex.split(cmd, posix=False))

    print("[*] Install End...")


def installAllFile():
    PATH = os.path.join(OUT, '*')

    for fileName in glob.glob(PATH):
        if not os.path.isfile(fileName):
            continue

        installer(fileName)