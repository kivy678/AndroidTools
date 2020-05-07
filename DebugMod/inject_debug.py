# -*- coding:utf-8 -*-

import os
import glob
import uuid
import shutil
import shlex
import subprocess

from .settings import *

from bs4 import BeautifulSoup


def readManifest():

    try:
        with open(MANIFEST) as fr:
            soup = BeautifulSoup(fr, "lxml-xml")
            soup.application['android:debuggable'] = 'true'

            with open(MANIFEST_WRITE, "w", encoding='utf-8') as fw:
                fw.write(str(soup))
    except Exception as e:
        print(e)
        exit()


def fileManger():

    try:
        os.remove(MANIFEST)
        os.rename(MANIFEST_WRITE, MANIFEST)
    except Exception as e:
        print(e)
        return False


def injection(_file):

    print("[*] start decode: " + _file)
    cmd = f"java -jar {APK_TOOL} d -f -o {DECODE_DIR} {_file}"
    subprocess.call(shlex.split(cmd, posix=False))

    readManifest()
    fileManger()

    print("[*] start build: " + _file)
    cmd = f"java -jar {APK_TOOL} b -f -o {OUT_APK} {DECODE_DIR}"
    subprocess.call(shlex.split(cmd, posix=False))

    print("[*] sign code: " + _file)
    KEY_APK = os.path.join(OUT, _file)

    cmd = f"java -jar {signapk} {certificate} {pk8} {OUT_APK} {KEY_APK}"
    subprocess.call(shlex.split(cmd, posix=False))

    print("[*] File Cleanup: " + _file)
    shutil.rmtree(DECODE_DIR, ignore_errors=True)
    os.remove(OUT_APK)

    print("injection End...")


def injectionAllFile():
    PATH = os.path.join(IN, '*')

    for fileName in glob.glob(PATH):
        if not os.path.isfile(fileName):
            continue

        injection(fileName)