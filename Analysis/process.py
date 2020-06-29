# -*- coding:utf-8 -*-

###########################################################################################

import re
from io import StringIO

from Analysis import app

from util.Logger import LOG
from cmd import dev

#from time import perf_counter as pc

###########################################################################################


class ProcessInfor:
    def __init__(self):
        self._pid = None
        self._tpid = None

    def getPid(self, pkgName):
        result = "'{print $2}'"
        cmd = f"ps | grep {app.pkgName} | awk {result}"
        pid = dev.runCommand(cmd, shell=True)

        if pid == str():
            LOG.info(f"{'':>5}Not Running Process.")
            self._pid = False

        return self._pid

    def getTPid(self, pid):
        if (not self._pid is None) or (not self._pid is False):
            cmd = f"cat /proc/{pid}/status"
            m = dev.runCommand(cmd, shell=True)

            r = re.compile(r".*^TracerPid:\s*(\d*)", re.M | re.S)
            with StringIO(m) as sio:
                self._tpid = r.match(sio.getvalue()).group(1)

    def getMaps(self, pid, s):
        cmd = f"cat /proc/{pid}/maps"
        m = dev.runCommand(cmd, shell=True)

        r = re.compile(rf"^.*{s}.*", re.M)
        with StringIO(m) as sio:
            for row in r.findall(sio.getvalue()):
                print(row)
