# -*- coding:utf-8 -*-

###########################################################################################

import pandas as pd

import elfformat
from module.mobile.DeviceManager.device import EMULATOR
from module.mobile.cmd import shell

from module.database import df_dev_lib, df_lib

from util.Logger import LOG
from util.fsUtils import Join, BaseName

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
        for i in self.fileList:
            rows = pd.Series({
                "model": self.dev.model,
                "lib": BaseName(i),
            })
            df_dev_lib.DATA_FRAME = df_dev_lib.DATA_FRAME.append(rows, ignore_index=True)
            df_dev_lib.DATA_FRAME = df_dev_lib.DATA_FRAME.drop_duplicates(subset=['lib'], keep='first')

            df_dev_lib.saveCSV()

            idx = df_dev_lib.DATA_FRAME[df_dev_lib.DATA_FRAME["lib"] == BaseName(i)].index.to_list()[0]

            self.iterGetData(idx)

        return None


    def iterGetData(self, fk):
        cmd = f"adb pull {self.fileList[0]} {DATA_DIR}"
        shell.runCommand(cmd, shell=False)

        libc_path = Join(DATA_DIR, "libc.so")
        for i in elfformat.parser(libc_path, 'dS', 'f').strip().split('\n'):
            v = i.rstrip('\r').split()

            try:
                if v[3] == "FUNC":
                    rows = pd.Series({
                        "func": v[5],
                        "addr": v[1],
                        "lib_fk": fk
                    })
                    df_lib.DATA_FRAME = df_lib.DATA_FRAME.append(rows, ignore_index=True)
                    df_lib.saveCSV()

            except IndexError as e:
                continue

        return None
