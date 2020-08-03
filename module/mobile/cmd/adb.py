# -*- coding:utf-8 -*-

#############################################################################

from module.mobile.cmd import shell

#############################################################################

__all__ = [
    "adbDevices",
    "adbRestart",
    "getModel",
    "getSystem",
    "getBootImage",
]

#############################################################################


def adbDevices():
    stdout = shell.runCommand("adb devices")
    return True if r'\n' in repr(stdout) else False


def adbRestart():
    shell.runCommand("adb kill-server")
    shell.runCommand("adb start-server")
    return None


#############################################################################

def getModel():
    stdout = shell.runCommand("getprop ro.product.model", shell=True)
    return stdout

def getSystem():
	stdout = shell.runCommand("getprop ro.product.cpu.abi", shell=True)
	return stdout.replace('-', '_')

def getBootImage(api):
    if api < 7:
        stdout = shell.runCommand("getprop ro.build.fingerprint", shell=True)
    else:
        stdout = shell.runCommand("getprop ro.bootimage.build.fingerprint", shell=True)

    return stdout