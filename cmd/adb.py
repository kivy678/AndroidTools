# -*- coding:utf-8 -*-

#############################################################################

from cmd.shell import SHELL

#############################################################################

__all__=[
    'DEVICE_DEBUG', 
]

class DEVICE_BASIS(SHELL):
    _PLATFORM_ = {
        "x86": "x86", "x64": "x64",
        "armeabi_v7a": "arm", "arm64_v8a": "arm64"
    }

    _platform   = None
    _su         = None

    def __init__(self, *args, **kwargs):
        self.runCommand("adb root", shell=False)
        self._su        = self.isRoot()
        self._platform  = self.getSystem()

    def __getattr__(self, key):
        try:
            return self._PLATFORM_[key]
        except KeyError as e:
            return None

    def shellmode(f):
        def inner(*args, **kwargs):
            self, cmd = args

            try:
                if self.su and kwargs['su'] == True:
                    cmd = 'su -c ' + repr(cmd)
            except KeyError:
                pass

            if kwargs['shell'] == True:
                cmd = 'adb shell ' + cmd

            return f(self, cmd, **kwargs)
        return inner


    @shellmode
    def runCommand(self, cmd, shell=False, su=False):
        return super().runCommand(cmd)


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

    @property
    def platform(self):
        return getattr(self, self._platform)


    @property
    def su(self):
        return self._su

class DEVICE_DEBUG(DEVICE_BASIS):
    pass
