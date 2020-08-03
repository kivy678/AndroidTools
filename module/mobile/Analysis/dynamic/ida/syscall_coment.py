# -*- coding:utf-8 -*-

import csv

from idaapi import *
from idautils import *
from idc import *


PATH = r''

def getRef(start_addr):
    for xref in XrefsTo(start_addr, 1):
        if xref.type == 21:
            continue
        else:
            yield xref.frm


def searchName(_name):
    for func in Names():
        if func[1] == _name:
            for addr in getRef(func[0]):

                num = int(GetOpnd(addr - 4, 1).lstrip('#'), 16)
                with open(PATH, 'r') as fr:
                    cr = csv.reader(fr, delimiter=',', quotechar="'", quoting=csv.QUOTE_ALL)

                    for row in cr:
                        if int(row[0]) == num:
                            MakeComm(addr, row[1])

searchName("syscall")
