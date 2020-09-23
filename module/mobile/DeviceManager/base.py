# -*- coding:utf-8 -*-

#############################################################################

from module.mobile.cmd import shell, adb

#############################################################################


class DEVICE_BASIS:
    _PLATFORM_ = {
        "x86": "x86", "x64": "x64",
        "armeabi_v7a": "arm", "arm64_v8a": "arm64"
    }

    _isConnect  = None
    _platform   = None
    _sdk        = None
    _su         = None

    def __init__(self, *args, **kwargs):
        self._isConnect = adb.adbDevices()
        if self._isConnect:
            self._platform  = adb.getSystem()
            self._sdk       = adb.getSdk()
            self._su        = self.isRoot()

    def __getattr__(self, key):
        try:
            return self._PLATFORM_[key]
        except KeyError as e:
            return None

    @classmethod
    def getPlatform(cls):
        return cls()

    @property
    def isConnect(self):
        return self._isConnect

    @property
    def platform(self):
        return self._platform

    @property
    def sdk(self):
        return self._sdk

    @property
    def su(self):
        return self._su

    def isRoot(self):
        stdout = shell.runCommand("if [ -f /system/bin/su ]; then echo True; fi", shell=True)
        if stdout == "":
            stdout = shell.runCommand("if [ -f /sbin/su ]; then echo True; fi", shell=True)

        if stdout == 'True':
            return True
        else:
            return False
