# -*- coding:utf-8 -*-

###########################################################################################

import re
from io import StringIO

from module.mobile.cmd import shell

from util.Logger import LOG

###########################################################################################


class ProcessInfor:
    def __init__(self):
        self._pid = None
        self._tpid = None


    def getPid(self, pkgName) -> list:
        result = "'{print $2}'"
        cmd = f"ps | grep {pkgName} | awk {result}"
        pid = shell.runCommand(cmd, shell=True)
        self._pid = pid.split()

        if pid == str():
            LOG.info(f"{'':>5}Not Running Process.")
            self._pid = False

        return self._pid


    def getTPid(self, pid):
        if (not self._pid is None) or (not self._pid is False):
            cmd = f"cat /proc/{pid}/status"
            m = shell.runCommand(cmd, shell=True)

            r = re.compile(r".*^TracerPid:\s*(\d*)", re.M | re.S)
            with StringIO(m) as sio:
                self._tpid = r.match(sio.getvalue()).group(1)

            return self._tpid


    def getMaps(self, pid, filter=''):
        cmd = f"cat /proc/{pid}/maps"
        m = shell.runCommand(cmd, shell=True)

        r = re.compile(rf"^.*{filter}.*", re.M)
        with StringIO(m) as sio, StringIO() as wio:
            for row in r.findall(sio.getvalue()):
                wio.write(row)

            return wio.getvalue()
