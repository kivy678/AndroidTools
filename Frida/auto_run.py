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

    def __getattr__(self, key):
        try:
            return self._PLATFORM_[key]
        except KeyError as e:
            return None

    def __init__(self, *args, **kwargs):
        subp(self.parseString("adb root"),
             stdout=subprocess.PIPE)

    def runCommand(self, cmd):
        subp(self.parseString(cmd), stdout=subprocess.PIPE)

    def parseString(self, cmd):
        s = shlex.shlex(cmd)
        s.whitespace_split = True

        return s

    def getSystem(self):
        with subp(self.parseString("adb shell getprop ro.product.cpu.abi"), stdout=subprocess.PIPE) as proc:
            stdin, stdout = proc.communicate()

        return stdin.decode("utf-8").strip().replace('-', '_')


adb_mod = ADBMODE()
platform = getattr(adb_mod, adb_mod.getSystem())

adb_mod.runCommand(
    "adb push " + r"TOOL\frida-server-12.7.15-android-" + platform + " /data/local/tmp")
adb_mod.runCommand(
    "adb shell chmod 755 /data/local/tmp/frida-server-12.7.15-android-" + platform)
adb_mod.runCommand(
    "adb shell nohup /data/local/tmp/frida-server-12.7.15-android-" + platform + ' &')
