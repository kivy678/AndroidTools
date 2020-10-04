# -*- coding:utf-8 -*-

##################################################################################################

from flask.views import MethodView
from flask import render_template

from web.views.prefer import view

from common import getSharedPreferences
from webConfig import SHARED_PATH

##################################################################################################

sp = getSharedPreferences(SHARED_PATH)

##################################################################################################


class SetupPage(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):

        platform = [
            ('OS', sp.getString('OS')),
            ('ARCH', sp.getString('ARCH')),
        ]

        dir_path = [
            ('WORKING', sp.getString('WORKING_DIR')),
            ('DATA', sp.getString('DATA_DIR')),
            ('SAMPLE', sp.getString('SAMPLE_DIR')),
            ('DECODE', sp.getString('DECODE_DIR')),
            ('ANALYSIS', sp.getString('ANALYSIS_DIR')),
            ('TMP', sp.getString('TMP_DIR')),
        ]

        too_path = [
            ('JADX', sp.getString('JADX_PATH')),
            ('JUST_DECOMPILE', sp.getString('JUST_DECOMPILE_PATH')),
            ('IL2CPP_DUMPER', sp.getString('IL2CPP_DUMPER_PATH')),
            ('IDA', sp.getString('IDA_PATH')),
        ]

        return render_template(self.template_name,
                                platform=platform,
                                dir_path=dir_path,
                                too_path=too_path)


setup_page = SetupPage.as_view('set', template_name='prefer/setting.jinja')
view.add_url_rule('set', view_func=setup_page)
