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
        print(mode, ldName, appName)

        f = f'fetch_{mode}'

        if hasattr(self, f) is False:
            return redirect('/dev/index')

        return getattr(self, f)(ldName, appName)


    def fetch_list(self, ldName=None, appName=None):
        return f"<pre>{LDPlayer.list()}</pre>"


    def fetch_create(self, ldName=None, appName=None):
        LDPlayer.create(ldName)
        return f"생성 완료-{ldName}"


    def fetch_remove(self, ldName='', appName=None):
        LDPlayer.remove(ldName)
        return f"삭제 완료-{ldName}"


    def fetch_run(self, ldName, appName=None):
        LDPlayer.run(ldName)
        return f"LDPlayer 실행 완료-{ldName}"


    def fetch_quit(self, ldName='', appName=None):
        LDPlayer.quit(ldName)
        return f"LDPlayer 종료 완료-{ldName}"


    def fetch_runApp(self, ldName='', appName=''):
        LDPlayer.runApp(ldName, appName)
        return f"앱 실행 완료"


    def fetch_runKillApp(self, ldName='', appName=''):
        LDPlayer.runKillApp(ldName, appName)
        return f"앱 종료 완료"


ld_manager = LDPLAYER_MANAGER.as_view('manager', template_name='')
view.add_url_rule('manager/<mode>', view_func=ld_manager)
