# -*- coding:utf-8 -*-

################################################################################

from initialize.device import *

from cmd import dev

################################################################################


def setDevice():
    if dev.isConnect is False:
        print(f"{'[*]':<5}Not Running Device")
        return False

    if isCommit() is False:
        print(f"{'[*]':<5}Settings Start")

        print(f"{'':>5}1. Basis App Install Start")
        appInstaller()

        print(f"{'':>5}2. Cow Exploit Start")
        cowExploit()

        print(f"{'':>5}3. Frida Server Install Start")
        fridaServer()

        print(f"{'':>5}4. Android Server Install Start")
        androidServer()

        print(f"{'':>5}5. Commit To Device")
        commit()
        print(f"{'[*]':<5}Settings End")

    else:
        print("Has Initalize Device")
