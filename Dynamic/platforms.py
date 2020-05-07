# -*- coding:utf-8 -*-

import os
import subprocess
import shlex

subp = subprocess.Popen

class ADBMODE(object):
    _PLATFORM_ = {
        "x86": "x86", "x64": "x64",
        "armeabi_v7a": "arm", "arm64_v8a": "arm64"
    }

    _platform = None

    def __init__(self, *args, **kwargs):
        subp(self.parseString("adb root"),
             stdout=subprocess.PIPE)

    def __getattr__(self, key):
        try:
            return self._PLATFORM_[key]
        except KeyError as e:
            return None

    @classmethod
    def getPlatform(cls):
        adb_mod = ADBMODE()
        cls._platform = getattr(adb_mod, adb_mod.getSystem())

        return cls._platform

    def runCommand(self, cmd):

        with subp(self.parseString(cmd), stdout=subprocess.PIPE) as proc:
            try:
                return proc.communicate(timeout=3)[0].decode('utf-8').strip()
            except subprocess.TimeoutExpired:
                proc.kill()
                return proc.communicate()[0].decode('utf-8').strip()


    def parseString(self, cmd):
        s = shlex.shlex(cmd)
        s.whitespace_split = True

        return s

    def getSystem(self):
        with subp(self.parseString("adb shell getprop ro.product.cpu.abi"), stdout=subprocess.PIPE) as proc:
            stdin, stdout = proc.communicate()

        return stdin.decode("utf-8").strip().replace('-', '_')
