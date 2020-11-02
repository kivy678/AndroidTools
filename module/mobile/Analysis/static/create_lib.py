# -*- coding:utf-8 -*-

################################################################################

import elfformat

from util.fsUtils import *

from common import getSharedPreferences
from webConfig import SHARED_PATH

################################################################################

sp              = getSharedPreferences(SHARED_PATH)
DATA_DIR        = sp.getString('DATA_DIR')

################################################################################


def createLibrary(org_Path, lib_path):
    save_path   = Join(DATA_DIR, BaseName(org_Path) + '_created')

    org_fr      = open(org_Path, 'rb')
    lib_fr      = open(lib_path, 'rb')
    save_fw     = open(save_path, 'wb')

    for i in elfformat.parser(lib_path, 'p', 'm').strip().split('\n'):
        l = i.split()

        if (l[0] == 'LOAD') and (int(l[1], 16) is 0):
            mSize = int(l[5], 16)

            save_fw.write(lib_fr.read(mSize))
            save_fw.flush()

        elif (l[0] == 'LOAD') and (int(l[1], 16) is not 0):
            offset  = int(l[1], 16)
            addr    = int(l[2], 16)
            fSize   = int(l[4], 16)
            mSize   = int(l[5], 16)

            lib_fr.seek(addr)
            save_fw.seek(offset)
            save_fw.write(lib_fr.read(fSize))

            org_fr.seek(offset + fSize)
            save_fw.write(org_fr.read())


    org_fr.close()
    lib_fr.close()
    save_fw.close()

    return save_path
