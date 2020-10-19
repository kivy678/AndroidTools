# -*- coding:utf-8 -*-

###########################################################################################

import pandas as pd

import elfformat
from module.mobile.DeviceManager.device import EMULATOR
from module.mobile.cmd import shell

from module.database import df_dev_lib

from util.Logger import LOG
from util.fsUtils import Join

from common import getSharedPreferences
from webConfig import SHARED_PATH

################################################################################

sp                  = getSharedPreferences(SHARED_PATH)
DATA_DIR             = sp.getString('DATA_DIR')

################################################################################


class AnalysisData:
    def __init__(self, dev):
        self.dev = dev
        self.fileList = ["/system/lib/libc.so"]

    def getData(self):
        cmd = f"adb pull {self.fileList[0]} {DATA_DIR}"
        shell.runCommand(cmd, shell=False)

        libc_path = Join(DATA_DIR, "libc.so")
        for i in elfformat.parser(libc_path, 'dS').strip().split('\n'):
            v = i.rstrip('\r').split()

            try:
                if v[3] == "FUNC":
                    rows = pd.Series({
                        "lib": v[5],
                        "addr": v[1],
                        "model": self.dev.model
                    })
                    df_dev_lib.DATA_FRAME = df_dev_lib.DATA_FRAME.append(rows, ignore_index=True)
                    df_dev_lib.saveCSV()

            except IndexError as e:
                continue

        return None
