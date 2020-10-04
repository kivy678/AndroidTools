# -*- coding:utf-8 -*-

################################################################################

from flask.views import MethodView
from flask import render_template, request

from web.views.analysis import view_dynamic

from module.mobile.DeviceManager.process import ProcessInfor
from module.mobile.Analysis.dynamic.mview import getMemory

from module.mobile.cmd import shell

from web.session import getSession

################################################################################

#MEM_FILTER  = ['']
MEM_FILTER  = ['/data/data/', '/data/app/', 'libc.so']
HEAP_SEARCH = ['heap']

HOOK_ARM = [
    "04F01FE5",  # ldr   pc, [pc, #-4]
]

PLATFORM_SIZE = {"ARM": 4, "THUMB": 2, "X86": 1}

################################################################################


class MemoryMap(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        pkg = getSession('pkg')
        pid_list = self.getPid(pkg)

        if pid_list is None:
            return "앱을 실행하세요"

        if request.args:
            f               = request.args.get("choiceMemory")
            platform_size   = PLATFORM_SIZE[request.args.get("platform")]

            pid             = request.args.get("pid")
            start_addr      = request.args.get("GetStartAddr")
            size            = request.args.get("GetSizeAddr")
            pathed_data     = request.args.get("GetData")


            if f == "read":
                if (start_addr is '') or (size is ''):
                    return "시작 주소, 사이즈를 입력해주세요."
                else:
                    cmd = f"/data/local/tmp/ReadMemory {pid} {start_addr} {size}"
                    return f"<pre>{shell.runCommand(cmd, shell=True, encoder='unicode-escape')}</pre>"


            elif f == "write":
                if (start_addr is '') or (size is '') or (pathed_data is ''):
                    return "시작 주소, 사이즈, 데이터를 입력해주세요"
                else:
                    cmd = f"/data/local/tmp/WriteMemory {pid} {start_addr} {size} {pathed_data}"
                    return f"<pre>{shell.runCommand(cmd, shell=True, encoder='unicode-escape')}</pre>"


            elif f == "search":
                if (size is '') or (pathed_data is ''):
                    return "사이즈, 데이터를 입력해주세요."
                else:
                    start_addr, end_addr = [(i.start_addr, i.end_addr) for i in getMemory(pid, HEAP_SEARCH)][0]
                    cmd = f"/data/local/tmp/SearchMemory {pid} {start_addr} {end_addr} {size} {pathed_data}"

                    return f"<pre>{shell.runCommand(cmd, shell=True, encoder='unicode-escape')}</pre>"


            elif f == "hook":
                if (start_addr is '') or (size is ''):
                    return "시작주소, 끝주소를 입력해주세요."
                else:
                    cmd = f"/data/local/tmp/SearchMemory {pid} {start_addr} {size} {platform_size} {HOOK_ARM[0]}"
                    data = shell.runCommand(cmd, shell=True, encoder='unicode-escape')

                    if data == '':
                        return "없습니다."

                    output = list()
                    for hook_addr in data.rstrip().split('\r\n'):
                        start_addr = int(hook_addr, 16) + 0x4

                        cmd = f"/data/local/tmp/ReadMemory {pid} {start_addr:08x} 4"
                        opcode = shell.runCommand(cmd, shell=True, encoder='unicode-escape')
                        output.append(f"{hook_addr}\t{self.opcodeReverse(opcode)}")

                    return "<pre>" + '\n'.join(output) + "</pre>"


            elif f == "trace":
                if (start_addr is ''):
                    return "시작주소와 플랫폼을 입력해주세요."
                else:
                    cmd = f"/data/local/tmp/trace {pid} {start_addr} {platform_size}"
                    return "<pre>" + shell.runCommand(cmd, shell=True, encoder='unicode-escape') + "</pre>"


        data = list()
        for pid in pid_list:
            data.append((pid, iter(getMemory(pid, MEM_FILTER))))

        return render_template(self.template_name, enter=data)


    def post(self):
        start_addr  = request.form.get("start_addr")
        end_addr    = request.form.get("end_addr")
        pid         = request.form.get("pid")

        cmd = f"/data/local/tmp/GetMemory {pid} {start_addr} 50"            # 현재 힙 사이즈 = 가로 100 * 50 = 5000

        return f"<pre>{shell.runCommand(cmd, shell=True, encoder='unicode-escape')}</pre>"


    def getPid(self, pkg):
        pi = ProcessInfor()
        pid_list = pi.getPid(pkg)

        return pid_list


    def opcodeReverse(self, l):
        l = l.strip().split()
        l.reverse()

        return f"0x{''.join(l)}"


mmap = MemoryMap.as_view('mmap', template_name='analysis/dynamic/mmap.jinja')
view_dynamic.add_url_rule('mmap', view_func=mmap)
