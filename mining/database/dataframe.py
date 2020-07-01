# -*- coding:utf-8 -*-

##########################################################################

import pandas as pd
import numpy as np

from common.singleton import Singleton
from mining.database.structure import COLUMNS

from util.Logger import LOG
from util.fsUtils import Join

from settings import CACHE

##########################################################################


class DATAFRAME_EXCEPTION_HANDER(Exception):
    pass


class DATAFRAME(Singleton):
    def __init__(self):
        self._DATA_FRAME = None

        try:
            cf = pd.read_csv(Join(CACHE, ".data.csv"), sep=',', index_col=0)

            self._DATA_FRAME = pd.DataFrame(data=cf)
            self._DATA_FRAME = self._DATA_FRAME.where(pd.notnull(self._DATA_FRAME), '')
            LOG.info("Load Data.CSV")

            self._DATA_FRAME = self._DATA_FRAME[~self._DATA_FRAME.index.duplicated(keep='first')]

        except FileNotFoundError as e:

            self._DATA_FRAME = pd.DataFrame(columns=COLUMNS)
            LOG.info("Create Data Frame")

        LOG.info('Initialize DataFrame')

    def __getattr__(self, key):
        try:
            return self.__dict__[key]
        except KeyError as e:
            return None

    def readCache(self): pass

    @property
    def DATA_FRAME(self):
        return self._DATA_FRAME
