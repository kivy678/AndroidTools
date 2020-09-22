# -*- coding:utf-8 -*-

#############################################################################

import csv

from module.mobile.DeviceManager.process import ProcessInfor
from module.mobile.Analysis.dynamic.mview import getMemory
from module.mobile.cmd import shell

from util.fsUtils import Join
from util.Logger import LOG

from common import getSharedPreferences
from webConfig import SHARED_PATH

from web.session import getSession
from web.cache import setCache, getCache, clearCache

################################################################################

################################################################################


def getPid(pkg):
    pi = ProcessInfor()
    pid_list = pi.getPid(pkg)

    if pid_list is None:
        return "앱을 실행하세요"

    for pid in pid_list:
        return pid


def setBP(path, baddr, bp, size):
    pkg = getSession('pkg')
    pid = getPid(pkg)

    if isinstance(pid, str):
        return pid


    bp_addr = {}

    tmp_addr = list()
    with open(path, 'r') as fr:
        cr = csv.reader(fr, delimiter=',', quotechar="'", quoting=csv.QUOTE_ALL)
        next(cr)            # remove header

        for row in cr:
            #if row[0] is not '':
            tmp_addr.append(row[0])


    for start_addr in tmp_addr:
        start_addr = int(start_addr, 16) + int(baddr, 16)

        cmd = f"/data/local/tmp/ReadMemory {pid} {start_addr:08x} {size}"
        data = shell.runCommand(cmd, shell=True, encoder='unicode-escape')

        cmd = f"/data/local/tmp/WriteMemory {pid} {start_addr:08x} {size} {bp}"
        shell.runCommand(cmd, shell=True, encoder='unicode-escape')

        bp_addr.update({start_addr: (size, data)})

    setCache("BP", bp_addr)


def restoreBP():
    if getCache("BP") is None:
        return False

    pkg = getSession('pkg')
    pid = getPid(pkg)

    if isinstance(pid, str):
        return pid

    for k, v in getCache("BP").items():
        cmd = f"/data/local/tmp/WriteMemory {pid} {k:08x} {v[0]} {v[1]}"
        shell.runCommand(cmd, shell=True, encoder='unicode-escape')

    clearCache()
