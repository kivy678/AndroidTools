# -*- coding:utf-8 -*-

################################################################################

import glob

from module.mobile.cmd import shell

from util.util import zipDecompress
from util.fsUtils import *

from util.Logger import LOG

from webConfig import SET_WORK, SERVER_PATH, APP_PATH

################################################################################

class DEVICE_INSTALLER():
    def __init__(self, cpu):
        self._cpu = cpu
        self.clean()

    def __del__(self):
        self.clean()

    def commit(self):
        cmd = f"mkdir /data/local/tmp/.cache"
        shell.runCommand(cmd, shell=True)

        cmd = f"echo '1' > /data/local/tmp/.cache/AndroidDevice"
        shell.runCommand(cmd, shell=True)

    def isCommit(self):
        cmd = f"find /data/local/tmp -type d -name .cache"
        stdout = shell.runCommand(cmd, shell=True)

        if stdout == '':
            return False
        else:
            cmd = f"find /data/local/tmp/.cache -name AndroidDevice"
            stdout = shell.runCommand(cmd, shell=True)

            return True if stdout != '' else False

    def toolInstall(self):
        TOOL_PATH = Join(SET_WORK, f"strace")         # strace -s 65535 -fF -t -i -o dump.txt -p [pid]

        cmd = f"adb push {TOOL_PATH} /system/strace"
        shell.runCommand(cmd, shell=False)

        cmd = f"chmod 755 /system/strace"
        shell.runCommand(cmd, shell=True)


        cmd = f"adb push {TOOL_PATH} /data/local/tmp/strace"
        shell.runCommand(cmd, shell=False)

        cmd = f"chmod 755 /data/local/tmp/strace"
        shell.runCommand(cmd, shell=True)


    def fridaServer(self):
        TOOL_PATH = Join(
            SET_WORK, f"frida-server-12.7.15-android-{self._cpu}")
        cmd = f"adb push {TOOL_PATH} /system/frida-server"
        shell.runCommand(cmd, shell=False)

        cmd = f"chmod 755 /system/frida-server"
        shell.runCommand(cmd, shell=True)

        #cmd = f"nohup /system/frida-server"
        #shell.runCommand(cmd, shell=True, su=True)

        cmd = f"adb push {TOOL_PATH} /data/local/tmp/frida-server"
        shell.runCommand(cmd, shell=False)

        cmd = f"chmod 755 /data/local/tmp/frida-server"
        shell.runCommand(cmd, shell=True)

        #cmd = f"nohup /data/local/tmp/frida-server"
        #shell.runCommand(cmd, shell=True, su=True)

    def androidServer(self):
        TOOL_PATH = Join(SET_WORK, f"android_{self._cpu}_server")

        cmd = f"adb forward tcp:22222 tcp:22222"
        shell.runCommand(cmd, shell=False)

        cmd = f"adb push {TOOL_PATH} /data/local/tmp/android_server"
        shell.runCommand(cmd, shell=False)

        cmd = f"chmod 755 /data/local/tmp/android_server"
        shell.runCommand(cmd, shell=True)

        #cmd = f"nohup /data/local/tmp/android_server"
        #shell.runCommand(cmd, shell=True, su=True)

    def cowExploit(self):
        cmd = "adb push {0} /data/local/tmp".format(Join(SET_WORK, 'mprop'))
        print(cmd)
        shell.runCommand(cmd, shell=False)

        cmd = f"chmod 755 /data/local/tmp/mprop && cd /data/local/tmp && ./mprop ro.debuggable 1"
        shell.runCommand(cmd, shell=True)

        cmd = f"getprop ro.debuggable"
        shell.runCommand(cmd, shell=True)

    def appInstaller(self):
        for app in self.appDecompress():
            cmd = f"adb install {app}"
            shell.runCommand(cmd, shell=False)

    def appDecompress(self):
        for _path in glob.glob(Join(APP_PATH, '*')):
            _, app_name = PathSplit(_path)

            zipDecompress(_path, SET_WORK)

            yield Join(SET_WORK, app_name.replace('zip', 'apk'))

    def serverDecompress(self):
        for _path in glob.glob(Join(SERVER_PATH, '*')):
            _, server_name = PathSplit(_path)

            zipDecompress(_path, SET_WORK)

    def clean(self):
        Delete(SET_WORK)
        DirCheck(SET_WORK)
