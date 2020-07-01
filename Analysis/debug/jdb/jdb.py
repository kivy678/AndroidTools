# -*- coding:utf-8 -*-

#############################################################################

from cmd import dev

#############################################################################


def jdbStart():
    print(f"{'[*]':<5}Start jdb")

    _port = dev.runCommand(f"adb jdwp", shell=False)
    print(f"{'[*]':<5}jdwp number: {_port}")

    dev.runCommand(f"adb forward tcp:23947 jdwp:{_port}", shell=False)
    dev.runCommand(f"jdb -connect com.sun.jdi.SocketAttach:hostname=localhost,port=23947", shell=False)

    print(f"{'[*]':<5}jdwp END")
