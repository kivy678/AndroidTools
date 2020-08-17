# -*- coding:utf-8 -*-

##########################################################################

from flask.views import MethodView
from flask import render_template, request

from web.views.analysis import view

import disassemble

##########################################################################


class Disasm(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        if request.args:
            data = request.args['data']

            opcode = ''.join([f"\\x{opcode}" for opcode in data.split()]).encode()
            opcode = opcode.decode('unicode-escape').encode('ISO-8859-1')

            return disassemble.disasmX86(opcode)

        return render_template(self.template_name)


disasm = Disasm.as_view('disasm', template_name='analysis/disasm.jinja')
view.add_url_rule('disasm', view_func=disasm)
