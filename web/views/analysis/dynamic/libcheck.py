# -*- coding:utf-8 -*-

################################################################################

from flask.views import MethodView
from flask import render_template, request

from web.views.analysis import view_dynamic

from module.mobile.DeviceManager.process import ProcessInfor
from module.mobile.Analysis.dynamic.mview import getMemory

from module.mobile.cmd import shell

from web.session import getSession

from util.fsUtils import *

from common import getSharedPreferences
from webConfig import SHARED_PATH

from web.session import getSession

import elfformat

################################################################################

sp              = getSharedPreferences(SHARED_PATH)
DATA_DIR        = sp.getString('DATA_DIR')
DECODE_DIR        = sp.getString('DECODE_DIR')

#MEM_FILTER  = ['']
MEM_FILTER  = ['/data/data/', '/data/app/', 'libc.so']


ARCH_SIZE = {"ARM": 4, "THUMB": 2, "X86": 1}

################################################################################

class LIB_CHECK(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        pkg = getSession('pkg')
        pid_list = self.getPid(pkg)

        if pid_list is None:
            return "앱을 실행하세요"

        if request.args:
            pid             = request.args.get("pid")
            start_addr      = request.args.get("GetStartAddr")
            end_addr        = request.args.get("GetEndAddr")
            lib_name        = request.args.get("GetLibName")

            """
            if (start_addr is '') or (end_addr is '') or (lib_name is ''):
                return "시작주소와 끝주소, 라이브러리를 입력해주세요."
            else:
                cmd = f"/data/local/tmp/MemoryDumper {pid} {start_addr} {end_addr}"
                shell.runCommand(cmd, shell=True, encoder='unicode-escape')

                cmd = f"adb pull /data/local/tmp/dump.bin {DATA_DIR}/{lib_name}"
                shell.runCommand(cmd, shell=False)

            """

            analysis_path = Join(DECODE_DIR, getSession('fileName'), 'unzip')
            for _path in Walk(analysis_path):
                if BaseName(_path) == "libjiagu_x86.so":
                    for rows in elfformat.parser(_path, 'd').strip().split('\n'):
                        row = rows.strip('\r').split()
                        if row[0] == "PLTGOT":
                            addr = int(row[1], 16)

                        elif row[0] == "PLTRELSZ":
                            addr_size = int(row[1])


            return "개발 중"


        data = list()
        for pid in pid_list:
            data.append((pid, iter(getMemory(pid, MEM_FILTER))))

        return render_template(self.template_name, enter=data)


    def getPid(self, pkg):
        pi = ProcessInfor()
        pid_list = pi.getPid(pkg)

        return pid_list


libcheck = LIB_CHECK.as_view('libcheck', template_name='analysis/dynamic/libcheck.jinja')
view_dynamic.add_url_rule('libcheck', view_func=libcheck)
