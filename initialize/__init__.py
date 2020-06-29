# -*- coding:utf-8 -*-

from initialize.devices import *

def setDevice():
    if isRunning() is False:
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
        print("Has Run")
