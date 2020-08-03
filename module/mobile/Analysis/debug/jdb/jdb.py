# -*- coding:utf-8 -*-

#############################################################################

from cmd import dev

#############################################################################


def jdbStart():
    print(f"{'[*]':<5}Start jdb")

    _port = dev.runCommand(f"adb jdwp", shell=False)
    for port in _port.split():
        print(f"{'[*]':<5}jdwp number: {port}")

        dev.runCommand(f"adb forward tcp:23947 jdwp:{port}", shell=False)
        dev.runCommand(f"jdb -connect com.sun.jdi.SocketAttach:hostname=localhost,port=23947", shell=False)

    print(f"{'[*]':<5}jdwp END")


def DynamicServer():
    print(f"{'[*]':<5}Start Server")

    cmd = r"adb forward tcp:23946 tcp:23946"
    dev.runCommand(cmd, shell=False)

    cmd = f"nohup /data/local/tmp/android_server"
    dev.runCommand(cmd, shell=True, su=True)

    cmd = f"nohup /system/frida-server"
    dev.runCommand(cmd, shell=True, su=True)

    print(f"{'[*]':<5}End")
