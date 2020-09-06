# -*- coding:utf-8 -*-

##########################################################################

import subprocess as sub

from flask.views import MethodView
from flask import render_template, request

from web.views.analysis import view_static

from util.fsUtils import *
from util.hash import getMD5

from common import getSharedPreferences
from webConfig import SHARED_PATH, BASE_DIR

from web.session import getSession

from module.ipython.convES.pretreatment import pushES
from module.ipython.scriptjs import parserScriptJson

##########################################################################

sp                  = getSharedPreferences(SHARED_PATH)
DECODE_DIR          = sp.getString('DECODE_DIR')
DATA_DIR            = sp.getString("DATA_DIR")

RUN_PATH            = Join(BASE_DIR, "module", "ipython", "run.bat")
RUN_IL2CPP_PATH     = Join(BASE_DIR, "module", "ipython", "run_il2cpp.bat")

##########################################################################


def findFile(dir, fileName):
    for _path in Walk(dir):
        if PathSplit(_path)[1] == fileName:
            return _path


class IDA(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        data = list()
        analysis_path = Join(DECODE_DIR, getSession('fileName'), 'unzip')

        for _path in Walk(analysis_path):
            p = PathSplit(_path)[1]
            ext = SplitExt(p)[1]

            if p == "libil2cpp.so":
                continue
            elif ext == ".so":
                data.append(_path)

        data = map(lambda x: (x.replace(analysis_path, '')[1:], round(FileSize(x)/1024)), data)

        return render_template(self.template_name, enter=data)


    def post(self):
        DirCheck(DATA_DIR)

        analysis_path   = Join(DECODE_DIR, getSession('fileName'), 'unzip')
        lib_path        = Join(analysis_path, request.form.get('lib'))
        md5             = getMD5(lib_path)

        script = "getStringToES.py"
        DATA_PATH = Join(DATA_DIR, md5 + '_str.txt')
        sub.Popen(RUN_PATH + f" {script} {md5} {DATA_PATH} {lib_path}").wait()
        pushES(DATA_PATH, 'aosstrings')

        script = "getImportsToES.py"
        DATA_PATH = Join(DATA_DIR, md5 + '_imp.txt')
        sub.Popen(RUN_PATH + f" {script} {md5} {DATA_PATH} {lib_path}").wait()
        pushES(DATA_PATH, 'aosimports')

        script = "getFunctionsToES.py"
        DATA_PATH = Join(DATA_DIR, md5 + '_func.txt')
        sub.Popen(RUN_PATH + f" {script} {md5} {DATA_PATH} {lib_path}").wait()
        pushES(DATA_PATH, 'aosfunctions')


        Delete(DATA_DIR)

        return "데이터 처리 완료"


class IL2CPP(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        DirCheck(DATA_DIR)

        il2cpp_path = Join(DECODE_DIR, getSession('fileName'), 'il2cpp')
        jsonPath    = Join(il2cpp_path, 'script.json')

        unzip_path  = Join(DECODE_DIR, getSession('fileName'), 'unzip')
        lib_path    =findFile(unzip_path, 'libil2cpp.so')

        md5         = getMD5(lib_path)

        #script = "getStringToES.py"
        #DATA_PATH = Join(DATA_DIR, md5 + '_str.txt')
        #sub.Popen(RUN_IL2CPP_PATH + f" {jsonPath} {script} {md5} {DATA_PATH} {lib_path}").wait()
        #pushES(DATA_PATH, 'aosstrings')

        #script = "getImportsToES.py"
        #DATA_PATH = Join(DATA_DIR, md5 + '_imp.txt')
        #sub.Popen(RUN_IL2CPP_PATH + f" {jsonPath} {script} {md5} {DATA_PATH} {lib_path}").wait()
        #pushES(DATA_PATH, 'aosimports')

        script = Join(BASE_DIR, "module", "ipython", "getFunctionsToES.py")
        DATA_PATH = Join(DATA_DIR, md5 + '_func.txt')
        sub.Popen(RUN_IL2CPP_PATH + f" {jsonPath} {script} {md5} {DATA_PATH} {lib_path}").wait()
        pushES(DATA_PATH, 'aosfunctions')


        #Delete(DATA_DIR)

        return "데이터 처리 완료"


class IL2CPP_SCRIPTJS(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        DirCheck(DATA_DIR)

        il2cpp_path = Join(DECODE_DIR, getSession('fileName'), 'il2cpp')
        jsonPath    = Join(il2cpp_path, 'script.json')

        unzip_path  = Join(DECODE_DIR, getSession('fileName'), 'unzip')
        lib_path    = findFile(unzip_path, 'libil2cpp.so')

        es_json     = Join(DATA_DIR, 'data.txt')

        parserScriptJson(lib_path, jsonPath, es_json)
        pushES(es_json, 'aosfunctions')


        #Delete(DATA_DIR)

        return "데이터 처리 완료"


ida_view = IDA.as_view('ida', template_name='analysis/static/ida.jinja')
view_static.add_url_rule('ida', view_func=ida_view)

il2cpp_view = IL2CPP.as_view('ida/il2cpp', template_name='')
view_static.add_url_rule('ida/il2cpp', view_func=il2cpp_view)

il2cpp_script_view = IL2CPP_SCRIPTJS.as_view('ida/script', template_name='')
view_static.add_url_rule('ida/script', view_func=il2cpp_script_view)
