# -*- coding:utf-8 -*-

##########################################################################

import pandas as pd

from flask.views import MethodView
from flask import render_template

from web.views.device import view

from module.mobile.DeviceManager.device import EMULATOR
from module.database import df_dev

##########################################################################


class DEVICE_LIST(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        dev = EMULATOR.getPlatform()

        if dev.setup() is False:
            return "연결된 기기가 없습니다."

        rows = pd.Series({
            "model": dev.model,
            "cpu": dev.platform,
            "sdk": dev.sdk,
            "su": dev.su,
            "setup": dev.installer.isCommit()
        })
        df_dev.DATA_FRAME = df_dev.DATA_FRAME.append(rows, ignore_index=True)
        df_dev.DATA_FRAME = df_dev.DATA_FRAME[~df_dev.DATA_FRAME.duplicated(['model'], keep='first')]

        return render_template(self.template_name, enter=df_dev.DATA_FRAME)


device = DEVICE_LIST.as_view('list', template_name='device/list.jinja')
view.add_url_rule('list', view_func=device)
