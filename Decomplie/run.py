# -*- coding:utf-8 -*-

import os
import shutil
import subprocess
import shlex

from settings import *


def fileManger():
    try:
        if os.path.isdir(OUT):
            shutil.rmtree(OUT, ignore_errors=True)
    except Exception as e:
        print(e)
        return False

def parseString(cmd):
    s = shlex.shlex(cmd)
    s.whitespace_split = True

    return s

def runCommand(cmd):

    with subprocess.Popen(parseString(cmd), stdout=subprocess.PIPE) as proc:
        try:
            return proc.communicate(timeout=3)[0].decode('utf-8').strip()
        except subprocess.TimeoutExpired:
            proc.kill()
            return proc.communicate()[0].decode('utf-8').strip()


def decodeSmali():
    print("[*] Start BackSmail")
    fileManger()
    runCommand(f"java -jar {BACK_TOOL} -o {OUT} {IN}")

    print("[*] End BackSmail")


decodeSmali()
