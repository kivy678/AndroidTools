# -*- coding:utf-8 -*-

##########################################################################

from flask.views import MethodView
from flask import render_template, request
from flask import redirect

from web.views.device import view

from module.mobile.DeviceManager.device import LDPlayer
from module.database import df_dev

##########################################################################


class LDPLAYER_MANAGER(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self, mode=''):
        ldName  = request.args.get("ldName")
        appName = request.args.get("appName")

        f = f'fetch_{mode}'

        if hasattr(self, f) is False:
            return redirect('/dev/index')

        return getattr(self, f)(ldName, appName)


    def fetch_list(self, ldName=None, appName=None):
        return render_template(self.template_name, enter=LDPlayer.list())


    def fetch_create(self, ldName=None, appName=None):
        LDPlayer.create(ldName)
        return f"{ldName}-생성"


    def fetch_remove(self, ldName='', appName=None):
        LDPlayer.remove(ldName)
        return f"{ldName}-삭제"


    def fetch_run(self, ldName, appName=None):
        LDPlayer.run(ldName)
        return f"{ldName}-실행"


    def fetch_quit(self, ldName='', appName=None):
        LDPlayer.quit(ldName)
        return f"{ldName}-종료"


    def fetch_reboot(self, ldName='', appName=None):
        LDPlayer.reboot(ldName)
        return f"{ldName}-재시작"


    def fetch_runApp(self, ldName='', appName=''):
        LDPlayer.runApp(ldName, appName)
        return f"{appName}-앱 실행"


    def fetch_runKillApp(self, ldName='', appName=''):
        LDPlayer.runKillApp(ldName, appName)
        return f"{appName}-앱 종료"


ld_manager = LDPLAYER_MANAGER.as_view('manager', template_name='device/index.jinja')
view.add_url_rule('manager/<mode>', view_func=ld_manager)
