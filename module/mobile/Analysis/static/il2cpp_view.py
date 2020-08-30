# -*- coding:utf-8 -*-

#############################################################################

import re
import mmap

from io import StringIO

from collections import OrderedDict
from operator import itemgetter

from util.fsUtils import *
from util.hash import *
from util.parser import JSON

import disassemble

#############################################################################


def convSplit(s):
    d = list(s)

    return ' '.join(reversed([i+j for i, j in zip(d[::2], d[1::2])]))

def dis(data):
    opcode = ''.join([f"\\x{opcode}" for opcode in data.split()]).encode()
    opcode = opcode.decode('unicode-escape').encode('ISO-8859-1')

    return disassemble.disasmARM(opcode)


def view(jsons, cs_path):
    data = dict()
    String_Buffer  = StringIO()

    for content in jsons.split('\n'):
        j = JSON.loads(content)
        data[j["offset"]] = [j["ORG_BIN"], j["MOD_BIN"]]


    data = OrderedDict(sorted(data.items(), key=itemgetter(0), reverse=False))

    with open(Join(cs_path, "dump.cs"), 'rb', 0) as file, mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
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

                String_Buffer.write(f"Offset:0x{offset_before:X}\t\tFunctionName: {func}\n")
                String_Buffer.write(f"CMP1:\n{dis(convSplit(bin_org))}\nCMP2:\n{dis(convSplit(bin_mod))}\n")
                String_Buffer.write("*"*150)
                String_Buffer.write("\n")

            else:
                offset_before = offset_current


    content = String_Buffer.getvalue()
    String_Buffer.close()

    return content
