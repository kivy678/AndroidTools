# -*- coding:utf-8 -*-

import os
import glob
import uuid
import shutil
import shlex
import subprocess

from .settings import *

from bs4 import BeautifulSoup


def setDebug(package, dbg=True):
    try:
        mode = "set" if dbg else "clear"
        option = "-w" if dbg else ""

        cmd = f"adb shell am {mode}-debug-app {option} {package}"
        print(f"[*] {mode} debug {package}")

        subprocess.call(shlex.split(cmd, posix=False))

    except Exception as e:
        print(e)
        return False

    finally:
        print("[*] File Clean")
        shutil.rmtree(DECODE_DIR, ignore_errors=True)


def readManifest():
    try:
        with open(MANIFEST) as fr:
            soup = BeautifulSoup(fr, "lxml-xml")
            return soup.manifest.get("package")

    except Exception as e:
        print(e)
        exit()


def decode(_file):
    try:
        print("[*] start decode: " + os.path.split(_file)[1])
        cmd = f"java -jar {APK_TOOL} d -f -o {DECODE_DIR} {_file}"
        subprocess.call(shlex.split(cmd, posix=False))

        return readManifest()

    except Exception as e:
        return False

    finally:
        print("[*] File Clean")
        shutil.rmtree(DECODE_DIR, ignore_errors=True)


def getPackageName():
    PATH = os.path.join(IN, '*')

    for fileName in glob.glob(PATH):
        if not os.path.isfile(fileName):
            continue

        yield (fileName, decode(fileName))