# -*- coding:utf-8 -*-

from .platforms import ADBMODE

def idaStart():
    # print(ADBMODE.getPlatform())
    adb_mod = ADBMODE()

    adb_mod.runCommand("adb forward tcp:23946 tcp:23946")
    adb_mod.runCommand("adb push " + r"TOOL\android_server" + " /data/local/tmp")
    adb_mod.runCommand("adb shell chmod 755 /data/local/tmp/android_server")

    print("start android_server")
    adb_mod.runCommand('adb shell su -c "nohup /data/local/tmp/android_server &"')

    print("End IDA")


def jdbStart():
    adb_mod = ADBMODE()
    _port = adb_mod.runCommand("adb jdwp")
    print(f"[*] jdwp number: {_port}")

    adb_mod.runCommand(f"adb forward tcp:23947 jdwp:{_port}")
    adb_mod.runCommand(f"jdb -connect com.sun.jdi.SocketAttach:hostname=localhost,port=23947")

    print("End JDB")
