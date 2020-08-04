# -*- coding:utf-8 -*-

###########################################################################################

import os
import sys

import frida

from util.fsUtils import Join
from webConfig import ANALYSIS_PATH

from util.Logger import LOG
from web.cache import lpush

###########################################################################################

JS_PATH = Join(ANALYSIS_PATH, "frida", "js", "libc.js")

###########################################################################################


class FridaRun:
    def __init__(self, stream):
        self.stream = stream

    def on_message(self, message, data):
        if message["type"] == "send":
            print(repr(message["payload"]["return"]))
        else:
            LOG.info(message)


    def Hook(self, _PACKAGE_NAME):
        with open(JS_PATH, 'r') as fr:
            jscode = fr.read()

        try:
            device = frida.get_usb_device(timeout=10)
            pid = device.spawn([_PACKAGE_NAME])
            LOG.info(f"App is starting ... pid : {pid}")

            process = device.attach(pid)
            device.resume(pid)

            script = process.create_script(jscode)
            script.on('message', self.on_message)
            LOG.info('[*] Running Hooking App')
            script.load()
            #sys.stdin.read()

        except Exception as e:
            LOG.info(e)
            LOG.info("Exception END...")

        LOG.info("[*] End Hooking App")


    def attachHook(self, _PACKAGE_NAME):
        with open(JS_PATH, 'r') as fr:
            jscode = fr.read()

        try:
            device = frida.get_usb_device(timeout=10)
            process = device.attach(_PACKAGE_NAME)
            LOG.info(f"App is Attaching ... pid : {process}")

            script = process.create_script(jscode)
            script.on('message', self.on_message)
            LOG.info('[*] Running Hooking App')
            script.load()
            #sys.stdin.read()

        except Exception as e:
            LOG.info(e)
            LOG.info("Exception END...")

        LOG.info("[*] End Hooking App")
