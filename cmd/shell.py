# -*- coding:utf-8 -*-

#############################################################################

import subprocess
import shlex

subp = subprocess.Popen

#############################################################################

class SHELL(object):
    def runCommand(self, cmd):
        with subp(self.parseString(cmd), stdout=subprocess.PIPE) as proc:
            try:
                return proc.communicate(timeout=20)[0].decode('utf-8').strip()
            except subprocess.TimeoutExpired:
                proc.kill()
                return proc.communicate()[0].decode('utf-8').strip()

    def parseString(self, cmd):
        s = shlex.shlex(cmd)
        s.whitespace_split = True

        return s
