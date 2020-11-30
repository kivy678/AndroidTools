# -*- coding:utf-8 -*-

##################################################################################################

import os
import ida_auto

import idaapi
import idautils
import idc

from Logger import LOG

##################################################################################################

if len(idc.ARGV) != 5:
    LOG.info("[*] [application] [HOST] [PORT] [PID] [SAVE_PATH]")
    idc.qexit(0)
else:
    HOST        = idc.ARGV[1]
    PORT        = int(idc.ARGV[2])

    PID         = int(idc.ARGV[3])
    SAVE_PATH   = idc.ARGV[4]

##################################################################################################
# 리눅스 원격 디버깅 설정

LOG.info("Start Debugging")
#ida_auto.auto_wait()

idaapi.set_processor_type("metapc", idaapi.SETPROC_LOADER | idaapi.SETPROC_IDB)

idaapi.set_remote_debugger(HOST, None, PORT)
if idaapi.load_debugger('linux', 1) is False:
    LOG.info("Load Debugger Failed")
    idc.qexit(0)
else:
    LOG.info("Load Debugger success")

if idaapi.attach_process(PID, -1) is False:
    LOG.info("Attach Failed")
    idc.qexit(0)
else:
    LOG.info("{0} Attach success".format(PID))

idaapi.wait_for_next_event(idaapi.WFNE_CONT, -1)

##################################################################################################

TRACE_MMAP              = "mmap"
DEX_SIG                 = "6465780A303335"

MMAP_ADDR               = None
mmap_addr_dict          = dict()
renew_mmap_addr_dict    = dict()

def MemToFile(fp, ptr, size):
    with open(fp, 'wb') as fd:
        fd.write(idc.get_bytes(ptr, size))
        fd.flush()

##################################################################################################
# mmap + 0x4F는 할당 작업이 끝난 후 메모리 할당 주소를 반환하는 주소이며, BP를 걸어준다.

MMAP_ADDR = idc.get_name_ea_simple(TRACE_MMAP) + 0x4F
idc.add_bpt(MMAP_ADDR, 0, idaapi.BPT_DEFAULT)

##################################################################################################

limit = 0
while True:
    if (idaapi.get_process_state() is idaapi.DSTATE_NOTASK) or limit > 100:         # 스레드가 죽을 경우와 프로세스가 running될 경우의 조건문
        break

    idaapi.continue_process()
    dbg_event = idaapi.wait_for_next_event(idaapi.WFNE_SUSP, -1)                    # suspend 이벤트가 발생할때 까지 블로킹

    try:
        if dbg_event is idaapi.BREAKPOINT:
            if idaapi.get_ip_val() == MMAP_ADDR:
                eax = idc.get_reg_value('eax')

                if eax in mmap_addr_dict:
                    continue

                if (idc.get_segm_attr(eax, idc.SEGATTR_PERM) & idaapi.SEGPERM_WRITE == 0x0) and                 \
                    (idc.get_segm_attr(eax, idc.SEGATTR_PERM) & idaapi.SEGPERM_EXEC == idaapi.SEGPERM_EXEC) and \
                    (idaapi.segtype(eax) & idaapi.SEG_DATA == 0x0):
                    continue                                                        # 불필요한 세그먼트 영역 제외


                if eax > 0x1:
                    size = idc.get_segm_attr(eax, idc.SEGATTR_END) - idc.get_segm_attr(eax, idc.SEGATTR_START)
                    mmap_addr_dict.update({eax: size})


                renew_mmap_addr_dict = mmap_addr_dict
                for _addr, _size in mmap_addr_dict.items():
                    if idaapi.getseg(_addr) is None:                                # munmap 된 세그먼트는 제외
                        del(renew_mmap_addr_dict[_addr])
                        continue

                    if idc.get_bytes(_addr, 7).encode('hex').upper() == DEX_SIG:
                        LOG.info(hex(_addr) + ': ' + hex(_size))

                        MemToFile(os.path.join(SAVE_PATH, hex(_addr) + '.dex'), _addr, _size)
                        del(renew_mmap_addr_dict[_addr])

                mmap_addr_dict = renew_mmap_addr_dict

                limit = 0

            else:
                limit += 1                                                          # mmap이 더이상 없을 경우 탈출

        elif dbg_event is idaapi.EXCEPTION:
            LOG.info('except')
            break

    except AssertionError as e:
        LOG.info(e)


LOG.info("***************************** Main End *****************************")
idc.qexit(0)
