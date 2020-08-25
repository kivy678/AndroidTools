# -*- coding:utf-8 -*-

#############################################################################

import os
import re

import struct

from util.fsUtils import *
from util.hash import *

try: import simplejson as json
except ImportError: import json

#############################################################################

BASE        = r'C:\tmp\data'
MOD_FILE    = r'C:\tmp\a\decode\grow-castle-mod_1.24.2-android-1.com.apk\unzip\lib\armeabi-v7a\libil2cpp.so'
ORG_FILE    = r'C:\tmp\a\decode\obase.apk\unzip\lib\armeabi-v7a\libil2cpp.so'

REPORT_FILE = Join(BASE, 'report.txt')

#############################################################################

class ESCAPE_CONDITION(Exception):
    pass

STRIP_HEX = [r'0xE3A0..00', r'0xE12FFF1E', r'0xE320F000']
DETECTED_HEX = [r'0xE320F000',                  # NOP
                r'0xE3A00000 0xE12FFF1E',       # mov R0, #0; BX LR                 00 00 a0 e3 1e ff 2f e1
                r'0xE0400000 0xE12FFF3E',       # sub r0, r0, r0; BLX LR            00 00 40 e0 3e ff 2f e1
                r'0xE3E00102 0xE12FFF1E',       # mov R0, #0x7FFFFFFF; BX LR        02 01 e0 e3 1e ff 2f e1
                r'0xE3E004FF 0xE12FFF1E',       # MOV R0, #0xFFFFFF; BLX LR         ff 04 e0 e3 1e ff 2f e1
                r'0xFEDEFFE7',                  # TRAP
]

#ORG_COMILE_HEX = map(lambda x: x, STRIP_HEX)           # python3.x Stateful iterators may be only consumed once
ORG_COMILE_HEX = [re.compile(x) for x in STRIP_HEX]

#############################################################################

def isSizeSame(opath, hpath):
    return True if GetSize(opath) == GetSize(hpath) else False

def getULong(fr):
    content = fr.read(4)
    return struct.unpack("<L", content)[0] if content else None


def longToHex(v):
    return '0x{:X}'.format(v)

if not isSizeSame(MOD_FILE, ORG_FILE):
    print('not same size')
    exit()


f_mod   = open(MOD_FILE, 'rb')
f_org   = open(ORG_FILE, 'rb')

fw      = open(REPORT_FILE, 'w')

while True:
    bin_mod = getULong(f_mod)
    bin_org = getULong(f_org)

    if (bin_mod is None) or (bin_org is None):
        break


    try:
        if bin_mod != bin_org:
            for p in ORG_COMILE_HEX:
                if p.match(longToHex(bin_org)):
                    raise ESCAPE_CONDITION(longToHex(bin_org))

            json_encoder = {"offset": f_mod.tell()-4, "ORG_BIN": bin_org, "MOD_BIN": bin_mod}
            json.dump(json_encoder, fw)
            fw.write('\n')
            fw.flush()

    except ESCAPE_CONDITION as e:
        #print('ESCAPE:', e)
        pass


f_mod.close()
f_org.close()
fw.close()


print('Main done...')
