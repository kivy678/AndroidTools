# -*- coding:utf-8 -*-

#############################################################################

import os
import subprocess
import shlex

subp = subprocess.Popen

#############################################################################

__all__=[
    'DEVICE_DEBUG', 
]

class DEVICE_BASIS(object):
    _PLATFORM_ = {
        "x86": "x86", "x64": "x64",
        "armeabi_v7a": "arm", "arm64_v8a": "arm64"
    }

    _platform   = None
    _su         = None

    def __init__(self, *args, **kwargs):
        subp(self.parseString("adb root"), stdout=subprocess.PIPE)
        self._su        = self.isRoot()
        self._platform  = self.getSystem()

    def __getattr__(self, key):
        try:
            return self._PLATFORM_[key]
        except KeyError as e:
            return None

    def shellmode(f):
        def inner(*args, **kwargs):
            if kwargs['shell'] == True:
                args = list(args)
                args[1] = "adb shell " + args[1]

            return f(*tuple(args), **kwargs)
        return inner

    @shellmode
    def runCommand(self, cmd, shell=False):
        with subp(self.parseString(cmd), stdout=subprocess.PIPE) as proc:
            try:
                return proc.communicate(timeout=3)[0].decode('utf-8').strip()
            except subprocess.TimeoutExpired:
                return proc.communicate()[0].decode('utf-8').strip()
            finally:
                proc.kill()

    def parseString(self, cmd):
        s = shlex.shlex(cmd)
        s.whitespace_split = True

        return s

    @classmethod
    def getPlatform(cls):
        return cls()

    def getSystem(self):
        stdin = self.runCommand("getprop ro.product.cpu.abi", shell=True)
        return stdin.replace('-', '_')

    def isRoot(self):
        stdin = self.runCommand("if [ -f /system/bin/su ]; then echo True; fi", shell=True)
        if stdin == 'True':
            self._su = True
        else:
            self._su = False

        return self._su


class DEVICE_DEBUG(DEVICE_BASIS):
    pass
