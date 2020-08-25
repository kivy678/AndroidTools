
from idaapi import *
from idautils import *
from idc import *

from os.path import join as Join

NAME = 'debug'

def MemToFile(fp, ptr, size):
	with open(fp, 'wb') as fd:
		fd.write(GetManyBytes(ptr, size))
		fd.flush()

ida_dbg.run_to(here())
def getSegInfo():
    for i in Segments():
        if SegName(i).startswith('debug'):
            size = SegEnd(i) - SegStart(i)
            if size <= 8192 or size > 1024*1024*30:
                continue
            yield (SegName(i), SegStart(i), size)

for name, start, size in getSegInfo():
    fp = r'C:\tmp\dump'
    MemToFile(Join(fp, name), start, size)

print('done....')
