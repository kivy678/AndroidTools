# -*- coding:utf-8 -*-

###########################################################################################

import os
import sys
import time

import frida

from module.frida.gui.Logger import getLogger

###########################################################################################

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
JS_PATH = os.path.join(BASE_DIR, "js", "merge.js")

###########################################################################################

class FridaRun:
    def __init__(self, pkg, stream=None):
        self._pkg    = pkg
        self._stream = stream

        self.script = None

    def on_message(self, message, data):
        if message["type"] == "send":
            self._stream.info(message["payload"] + '\n')
        else:
            self._stream.info(message)

        time.sleep(0.1)


    def Hook(self):
        with open(JS_PATH, 'r') as fr:
            jscode = fr.read()

        try:
            device = frida.get_usb_device(timeout=10)
            pid = device.spawn([self._pkg])
            print(f"App is starting ... pid : {pid}")

            process = device.attach(pid)
            device.resume(pid)

            self.script = process.create_script(jscode)
            self.script.on('message', self.on_message)

            print('[*] Running Hooking App')
            self.script.load()
            #sys.stdin.read()

        except Exception as e:
            print(e)
            print("Exception END...")


    def attachHook(self):
        with open(JS_PATH, 'r') as fr:
            jscode = fr.read()

        try:
            device = frida.get_usb_device(timeout=10)
            process = device.attach(self._pkg)
            print(f"App is Attaching ... pid : {process}")

            self.script = process.create_script(jscode)
            self.script.on('message', self.on_message)

            print('[*] Running Hooking App')
            self.script.load()
            #sys.stdin.read()

        except Exception as e:
            print(e)
            print("Exception END...")


    def dettachHook(self):
        if self.script:
            self.script.off('message', self.on_message)
            self.script.unload()

        print("[*] End Hooking App")

        return True
