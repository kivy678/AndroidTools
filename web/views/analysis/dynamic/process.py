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

MEM_FILTER = ['shell']

################################################################################


class MemoryMap(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        pkg = getSession('pkg')
        pid = self.getPid(pkg)

        if isinstance(pid, str):
            return pid

        if request.args:
            f = request.args.get("choiceMemory")

            start_addr = request.args.get("GetStartAddr")
            size = request.args.get("GetSizeAddr")
            pathed_data = request.args.get("GetData")


            if f == "read":
                if (start_addr is '') or (size is ''):
                    return "시작 주소, 사이즈를 입력해주세요."
                else:
                    cmd = f"/data/local/tmp/GetMemory {pid} {start_addr} {size}"
                    return f"<pre>{shell.runCommand(cmd, shell=True, encoder='unicode-escape')}</pre>"

            elif f == "write":
                if (start_addr is '') or (size is '') or (pathed_data is ''):
                    return "시작 주소, 사이즈, 데이터를 입력해주세요"
                else:
                    cmd = f"/data/local/tmp/WriteMemory {pid} {start_addr} {size} {pathed_data}"
                    return f"<pre>{shell.runCommand(cmd, shell=True, encoder='unicode-escape')}</pre>"


        data = getMemory(pid, MEM_FILTER)

        return render_template(self.template_name, enter=data)


    def post(self):
        start_addr = request.form.get("start_addr")
        end_addr = request.form.get("end_addr")

        pkg = getSession('pkg')

        pi = ProcessInfor()
        pid_list = pi.getPid(pkg)

        if pid_list is None:
            return "앱을 실행하세요"

        for pid in pid_list:
            cmd = f"/data/local/tmp/GetMemory {pid} {start_addr} 50"    # 현재 힙 사이즈 = 가로 100 * 50 = 5000

            return f"<pre>{shell.runCommand(cmd, shell=True, encoder='unicode-escape')}</pre>"




    def getPid(self, pkg):
        pi = ProcessInfor()
        pid_list = pi.getPid(pkg)

        if pid_list is None:
            return "앱을 실행하세요"

        for pid in pid_list:
            return pid


mmap = MemoryMap.as_view('mmap', template_name='analysis/dynamic/mmap.jinja')
view_dynamic.add_url_rule('mmap', view_func=mmap)
