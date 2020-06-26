# -*- coding:utf-8 -*-

import os
import sys

import frida


JS_PATH = os.path.join('js', "java.js")


def on_message(message, data):
    if message["type"] == "send":
        print("[*] {0}".format(message["payload"]))
    else:
        print(message)


def hook(_PACKAGE_NAME):
    with open(r'Analysis\frida\js\java.js', 'r') as fr:
        jscode = fr.read()

    try:
        device = frida.get_usb_device(timeout=10)
        pid = device.spawn([_PACKAGE_NAME])
        print(f"App is starting ... pid : {pid}")

        process = device.attach(pid)
        device.resume(pid)

        script = process.create_script(jscode)
        script.on('message', on_message)
        print('[*] Running Hooking App')
        script.load()
        sys.stdin.read()
    except Exception as e:
        print(e)
        print("Exception END...")

    print("[*] End Hooking App")

hook('com.cd.weixin')
