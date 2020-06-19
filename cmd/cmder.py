# -*- coding:utf-8 -*-

#############################################################################

from cmd.shell import SHELL

#############################################################################

class COMMANDER(SHELL):
    def javamode(f):
        def inner(*args, **kwargs):
            self, cmd = args

            if kwargs['java'] == True:
                cmd = 'java -jar ' + cmd

            return f(self, cmd, **kwargs)
        return inner


    @javamode
    def runCommand(self, cmd, java=False):
        return super().runCommand(cmd)
