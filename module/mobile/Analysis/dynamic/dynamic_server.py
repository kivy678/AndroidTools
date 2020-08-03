# -*- coding:utf-8 -*-

#############################################################################

from module.mobile.cmd import shell

#############################################################################


def jdbStart():
    print(f"{'[*]':<5}Start jdb")

    _port = shell.runCommand(f"adb jdwp", shell=False)
    for port in _port.split():
        print(f"{'[*]':<5}jdwp number: {port}")

        shell.runCommand(f"adb forward tcp:23947 jdwp:{port}", shell=False)
        shell.runCommand(f"jdb -connect com.sun.jdi.SocketAttach:hostname=localhost,port=23947", shell=False)

    print(f"{'[*]':<5}jdwp END")


def dynamicServer():
    print(f"{'[*]':<5}Start Server")

    cmd = r"adb forward tcp:22222 tcp:22222"
    shell.runCommand(cmd, shell=False)

    cmd = f"nohup /data/local/tmp/android_server &"
    shell.runCommand(cmd, shell=True, su=True)

    cmd = f"nohup /system/frida-server &"
    shell.runCommand(cmd, shell=True, su=True)

    print(f"{'[*]':<5}End Commnad")
