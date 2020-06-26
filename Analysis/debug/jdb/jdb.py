# -*- coding:utf-8 -*-

#############################################################################

from cmd import dev

#############################################################################

def jdbStart():
    _port = dev.runCommand(f"adb jdwp", shell=False)
    print(f"{'[*]':<5}jdwp number: {_port}")

    dev.runCommand(f"adb forward tcp:23947 jdwp:{_port}")
    dev.runCommand(f"jdb -connect com.sun.jdi.SocketAttach:hostname=localhost,port=23947")

    print(f"{'[*]':<5}jdwp END")
