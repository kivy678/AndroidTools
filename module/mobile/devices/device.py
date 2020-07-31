# -*- coding:utf-8 -*-

#############################################################################

from module.mobile.cmd import shell, adb
from module.mobile.devices.base import DEVICE_BASIS

#############################################################################

__all__=[
	"EMULATOR",
]

#############################################################################


class EMULATOR(DEVICE_BASIS):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self._model = None

    def setup(self):
        if self._isConnect:
            shell.runCommand("mount -o remount,rw /system", shell=True)
            shell.runCommand("mount -o remount,rw /", shell=True)

            self._model = adb.getModel()

            return True
        else:
            return False

    @property
    def model(self):
        return self._model


class GALAXY(DEVICE_BASIS):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

    def setup(self):
        shell.runCommand("adb root", shell=False)

        shell.runCommand("mount -o remount,rw /system", shell=True)
        shell.runCommand("mount -o remount,rw /", shell=True)
