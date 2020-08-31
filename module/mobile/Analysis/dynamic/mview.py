# -*- coding:utf-8 -*-

#############################################################################

from module.mobile.DeviceManager.process import ProcessInfor
from module.mobile.cmd import shell

#############################################################################


class MMAP_ATTRIBUTE:
    start_addr  = None
    end_addr    = None
    permission  = None
    sharedName  = None


def getMemory(pid, mFilter=['']):
    pi = ProcessInfor()
    mmap = pi.getMaps(pid, mFilter=mFilter).strip()

    mmap_list = list()
    for i in mmap.split("\r\n"):
        mmap = MMAP_ATTRIBUTE()
        data = i.strip().split()

        addr = data[0]
        mmap.permission = data[1]

        try:
            mmap.sharedName = data[5]
        except IndexError:
            mmap.sharedName = ''

        mmap.start_addr, mmap.end_addr = addr.split('-')

        mmap_list.append(mmap)

    return mmap_list
