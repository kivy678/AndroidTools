# -*- coding:utf-8 -*-

#############################################################################

from cmd.shell import SHELL

#############################################################################

class COMMANDER(SHELL):
    def mode(f):
        def inner(*args, **kwargs):
            self, cmd = args

            try:
                if kwargs['su'] == True:
                    cmd = 'su -c ' + repr(cmd)
            except KeyError:
                pass

            try:
                if kwargs['shell'] == True:
                    cmd = 'adb shell ' + cmd
            except KeyError:
                pass

            try:
                if kwargs['java'] == True:
                    cmd = 'java -jar ' + cmd
            except KeyError:
                pass

            return f(self, cmd, **kwargs)
        return inner

    @mode
    def runCommand(self, cmd, shell=False, java=False, su=False):
        return super().runCommand(cmd)
