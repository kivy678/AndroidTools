# -*- coding:utf-8 -*-

##########################################################################

import pandas as pd

from flask.views import MethodView
from flask import render_template, request

from web.views.device import view

from module.mobile.devices.install import DEVICE_INSTALLER
from module.database import df_dev

from util.Logger import LOG

##########################################################################


class DEVICE_WORKER(MethodView):
    def get(self):
        model = request.args['model']
        cpu = 'x86'
        dev = DEVICE_INSTALLER(cpu)

        if dev.isCommit() is False:
            LOG.info(f"{'[*]':<5}Settings Start")
            dev.serverDecompress()

            LOG.info(f"{'':>5}1. Basis App Install Start")
            dev.appInstaller()

            LOG.info(f"{'':>5}2. Cow Exploit Start")
            dev.cowExploit()

            LOG.info(f"{'':>5}3. Frida Server Install Start")
            dev.fridaServer()

            LOG.info(f"{'':>5}4. Android Server Install Start")
            dev.androidServer()

            LOG.info(f"{'':>5}5. Tool Install Start")
            dev.toolInstall()

            LOG.info(f"{'':>5}6. Commit To Device")
            dev.commit()

            LOG.info(f"{'[*]':<5}Settings End")
            df_dev.DATA_FRAME.loc[df_dev.DATA_FRAME['model'] == model, 'setup'] = True

            return "Settings End"
        else:
            LOG.info(f"{'[*]':<5}Has Initalize Device")

            return "Has Initalize Device"


device = DEVICE_WORKER.as_view('work')
view.add_url_rule('work', view_func=device)
