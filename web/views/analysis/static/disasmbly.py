# -*- coding:utf-8 -*-

##########################################################################

from flask.views import MethodView
from flask import render_template, request

from web.views.analysis import view_static

import disassemble

##########################################################################


class Disasm(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        if request.args:
            text        = request.args['text']
            platform    = request.args['platform']

            opcode      = ''.join([f"\\x{opcode}" for opcode in text.split()]).encode()
            opcode      = opcode.decode('unicode-escape').encode('ISO-8859-1')

            return getattr(disassemble, f'disasm{platform}')(opcode)

        return render_template(self.template_name)


disasm = Disasm.as_view('disasm', template_name='analysis/static/disasm.jinja')
view_static.add_url_rule('disasm', view_func=disasm)
