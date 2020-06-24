# -*- coding:utf-8 -*-

###########################################################################################

import os
import glob

from cmd import dev

###########################################################################################


def installer(_path):
    print(f"{'[*]':<5}start install: " + os.path.split(_path)[1])

    cmd = f"adb install -r {_path}"
    dev.runCommand(cmd, shell=False)

    print(f"{'[*]':<5}Install End")


def installAllFile(dpath):
    PATH = os.path.join(dpath, '*')

    for fileName in glob.glob(PATH):
        if not os.path.isfile(fileName):
            continue

        installer(fileName)
