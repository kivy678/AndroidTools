# -*- coding:utf-8 -*-

import os
import subprocess
import shlex

s = shlex.shlex("adb root")
s.whitespace_split = True
subprocess.Popen(s, stdout=subprocess.PIPE, shell=True)

s = shlex.shlex("adb push " + r"TOOL\frida-server-12.7.15-android-arm" + " /data/local/tmp")
s.whitespace_split = True
subprocess.Popen(s, stdout=subprocess.PIPE, shell=True)

s = shlex.shlex("adb shell chmod 755 /data/local/tmp/frida-server-12.7.15-android-arm")
s.whitespace_split = True
subprocess.Popen(s, stdout=subprocess.PIPE, shell=True)

s = shlex.shlex("adb shell /data/local/tmp/frida-server-12.7.15-android-arm &")
s.whitespace_split = True
subprocess.Popen(s, stdout=subprocess.PIPE, shell=True)
