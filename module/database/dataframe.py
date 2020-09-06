# -*- coding:utf-8 -*-

##########################################################################

import pandas as pd
import numpy as np

from common.singleton import Singleton
from module.database.structure import *

from util.Logger import LOG
from util.fsUtils import Join

from webConfig import CACHE

##########################################################################

class DATAFRAME_EXCEPTION_HANDER(Exception): pass

##########################################################################


class DATA_FRAME(Singleton):
    def __init__(self):
        self._DATA_FRAME = None

    def setup(self):
        pass

    def setCSV(self, fileName, COLUMN, dup=True):
        try:
            csv = pd.read_csv(Join(CACHE, fileName), sep=',', index_col=0)

            df = pd.DataFrame(data=csv)
            df = df.where(pd.notnull(df), '')
            LOG.info(f"Load {fileName}")

            if dup:
                df = df[~df.index.duplicated(keep='first')]

            return df

        except FileNotFoundError as e:
            LOG.info("Create Data Frame")
            return pd.DataFrame(columns=COLUMN)

        except DATAFRAME_EXCEPTION_HANDER as e:
            LOG.info(e)
            return False

    def saveCSV(self, fileName):
        try:
            self._DATA_FRAME.to_csv(Join(CACHE, f"{fileName}"), mode='w')

        except DATAFRAME_EXCEPTION_HANDER as e:
            LOG.info(e)
            return False

    def __getattr__(self, key):
        try:
            return self.__dict__[key]
        except KeyError as e:
            return None

    @property
    def DATA_FRAME(self):
        return self._DATA_FRAME

    @DATA_FRAME.setter
    def DATA_FRAME(self, DATA_FRAME):
        self._DATA_FRAME = DATA_FRAME


class DEVICE(DATA_FRAME):
    def setup(self):
        self._DATA_FRAME = self.setCSV(".dev.csv", DEV_COLUMNS)

    def saveCSV(self):
        super().saveCSV(".dev.csv")


class APPLICATION(DATA_FRAME):
    def setup(self):
        self._DATA_FRAME = self.setCSV(".app.csv", APP_COLUMNS)

    def saveCSV(self):
        super().saveCSV(".app.csv")


class UNITY(DATA_FRAME):
    def setup(self):
        self._DATA_FRAME = self.setCSV(".unity.csv", UNITY_COLUMNS)

    def saveCSV(self):
        super().saveCSV(".unity.csv")


class IL2CPP(DATA_FRAME):
    def setup(self):
        self._DATA_FRAME = self.setCSV(".il2cpp.csv", IL2CPP_COLUMNS)

    def saveCSV(self):
        super().saveCSV(".il2cpp.csv")


class OPCDOE(DATA_FRAME):
    def setup(self):
        self._DATA_FRAME = self.setCSV(".opcode.csv", OPCDOE_COLUMNS, dup=False)

    def saveCSV(self):
        super().saveCSV(".opcode.csv")

