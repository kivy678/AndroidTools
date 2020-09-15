# -*- coding:utf-8 -*-

##################################################################################################

import contextlib
import sys
import time
from io import StringIO

from tornado.websocket import WebSocketHandler

from module.mobile.Analysis.frida.run import FridaRun
from web.session import getSession

from util.Logger import LOG

##################################################################################################


class FridaDataStreamDataSocket(WebSocketHandler):
    def open(self):
        print("Socket opened.")
        frida_run = FridaRun(self)
        frida_run.attachHook("dz.angie.clean.master")
   
        #while True:
        buf = StringIO()

        with contextlib.redirect_stdout(buf):
            time.sleep(5)

        self.write_message(buf.getvalue())
        buf.close()


    def on_message(self, message):
        print("Received message: " + message)

    def on_close(self):
        print("Socket closed.")

    def streaming(self, message):
        self.write_message(message)
