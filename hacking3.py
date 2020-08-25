# -*- coding:utf-8 -*-

#############################################################################

import os
import re

import mmap

import struct

try: import simplejson as json
except ImportError: import json

from collections import OrderedDict
from operator import itemgetter

from util.fsUtils import *
from util.hash import *

import disassemble

#############################################################################

REPORT_FILE = Join(r'C:\tmp\data', 'report.txt')
DUMP_CSS = r'C:\tmp\a\decode\grow-castle-mod_1.24.2-android-1.com.apk\il2cpp\dump.cs'

#############################################################################

def convSplit(s):
    d = list(s)

    return ' '.join(reversed([i+j for i, j in zip(d[::2], d[1::2])]))

def dis(data):
    opcode = ''.join([f"\\x{opcode}" for opcode in data.split()]).encode()
    opcode = opcode.decode('unicode-escape').encode('ISO-8859-1')

    return disassemble.disasmARM(opcode)

data = dict()

with open(REPORT_FILE) as fr:
    for content in fr:
        j = json.loads(content)
        data[j["offset"]] = [j["ORG_BIN"], j["MOD_BIN"]]


data = OrderedDict(sorted(data.items(), key=itemgetter(0), reverse=False))

with open(DUMP_CSS, 'rb', 0) as file, mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
    offset_before = offset_current = 0
    for k in data:
        offset_current = k

        if (offset_current - offset_before) == 4:
            bin_org = f"{data[offset_before][0]:08x}{data[offset_current][0]:08x}"
            bin_mod = f"{data[offset_before][1]:08x}{data[offset_current][1]:08x}"

            pattern = f".*0x{offset_before:X}.*\n(.*)"
            m = re.search(pattern.encode(), s)

            if m:
                func = m.group(1).strip().decode('utf-8')
            else:
                func = ""

            print(f"Offset:0x{offset_before:X}\t\tFunctionName: {func}")
            print(f"Org:\n{dis(convSplit(bin_org))}\nMod:\n{dis(convSplit(bin_mod))}")
            print("*"*150)

        else:
            offset_before = offset_current
