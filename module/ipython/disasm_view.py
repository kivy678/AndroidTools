# -*- coding: utf-8 -*-

##################################################################################################

import struct
import disassemble

##################################################################################################


def convSplit(s):
    d = list(s)

    d = ([i+j for i, j in zip(d[::2], d[1::2])])
    for i in range(0,len(d),4):
        d[i:i+4] = list(reversed(d[i:i+4]))

    return ' '.join(d)


def dis(data):
    opcode = ''.join([f"\\x{opcode}" for opcode in data.split()]).encode()
    opcode = opcode.decode('unicode-escape').encode('ISO-8859-1')

    return disassemble.disasmARM(opcode)


def getULong(fr, p, size):
    fr.seek(p, 0)
    content = fr.read(size)
    return struct.unpack("<L", content)[0] if content else None


def longToHex(v):
    return '0x{:X}'.format(v)
