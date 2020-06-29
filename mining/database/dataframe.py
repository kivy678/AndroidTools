# -*- coding:utf-8 -*-

##########################################################################

import pandas as pd

from common.singleton import Singleton
from mining.database.structure import COLUMNS

from util.Logger import LOG

##########################################################################

class DATAFRAME_EXCEPTION_HANDER(Exception):
    pass

class DATAFRAME(Singleton):
    def __init__(self):
        self._DATA_FRAME = pd.DataFrame(columns=COLUMNS)

        LOG.info('Initialize DataFrame')

    def __getattr__(self, key):
        try:
            return self.__dict__[key]
        except KeyError as e:
            return None

    @property
    def DATA_FRAME(self):
        return self._DATA_FRAME

    @DATA_FRAME.setter
    def FILE_FRAME(self, _DATA_FRAME):
        self._DATA_FRAME = _DATA_FRAME
