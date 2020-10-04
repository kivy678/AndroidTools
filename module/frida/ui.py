# -*- coding:utf-8 -*-

##################################################################################################

import os
import kivy
from kivy.app import App
from kivy.lang import Builder

kivy.require('1.11.0')                                  # replace with your current kivy version !
kv = os.path.join(os.path.dirname(__file__), 'gui', 'widgets.kv')
Builder.load_file(kv, encoding='utf-8')

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.actionbar import ActionBar
from kivy.uix.label import Label

from kivy.properties import ObjectProperty, StringProperty

from gui.popup import CreatePopup
from gui.Logger import getLogger

from run import FridaRun

##################################################################################################


class HEADER_BAR(ActionBar):
    def __init__(self, **kwargs):
        super(HEADER_BAR, self).__init__(**kwargs)
        self.fr = None

    def show_load(self, app):
        ctb_id = app.ids.get('CONTEXT_BOX_ID')
        pop = CreatePopup()
        content = LoadDialog(ct_box=ctb_id, cancel=pop.dismiss_popup)
        pop.default_create(content, 'Load File')

    def on_version(self):
        content = f'\n\n      v0.3.0\n\n피드백 안 받습니다.\n    - kivy -'
        pop = CreatePopup(content)
        pop.removeButton('cancle')
        pop.create(pop, 'version')

    def on_exit(self):
        exit()

    def on_start(self, app):
        ctb_id = app.ids.get('CONTEXT_BOX_ID')
        cnt_id = ctb_id.ids.get('CONTENT_ID')
        cnt_id.text = ''

        LOG = getLogger('label.log', cnt_id)
        self.fr = FridaRun('com.hali.skinmate', LOG)
        self.fr.attachHook()

    def on_stop(self, app):
        ctb_id = app.ids.get('CONTEXT_BOX_ID')
        cnt_id = ctb_id.ids.get('CONTENT_ID')
        cnt_id.text = ''

        self.fr.dettachHook()


class LoadDialog(FloatLayout):
    ct_box = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def load_context(self, filelist):
        if len(filelist) == 0:
            self.cancel()
            return

        self.cancel()


class CONTEXT_BOX(BoxLayout):
    pass


class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)


class MainApp(App):
    def build(self):
        return RootWidget()


def AppRun():
    MainApp().run()


AppRun()
