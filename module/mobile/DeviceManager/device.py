# -*- coding:utf-8 -*-

__all__=[
    "EMULATOR",
]

#############################################################################

from module.mobile.cmd import shell, adb
from module.mobile.DeviceManager.base import DEVICE_BASIS
from module.mobile.DeviceManager.install import DEVICE_INSTALLER

#############################################################################

class EMULATOR(DEVICE_BASIS):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self._model = None
        self._installer = None

    def setup(self, dev_name=None):
        if self._isConnect:
            shell.runCommand("setenforce 0", shell=True)

            shell.runCommand("mount -o remount,rw /system", shell=True)
            shell.runCommand("mount -o remount,rw /", shell=True)

            self._model = adb.getModel()
            self._installer = DEVICE_INSTALLER(self._platform)

            return True

        else:
            return False

    @property
    def model(self):
        return self._model

    @property
    def installer(self):
        return self._installer


class GALAXY(DEVICE_BASIS):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

    def setup(self):
        shell.runCommand("adb root", shell=False)

        shell.runCommand("mount -o remount,rw /system", shell=True)
        shell.runCommand("mount -o remount,rw /", shell=True)


class LDPlayer(DEVICE_BASIS):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

    def cmd(self):
        shell.runCommand("dnconsole list", shell=False)
