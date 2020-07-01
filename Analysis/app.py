# -*- coding:utf-8 -*-

###########################################################################################

import pandas as pd

from util.fsUtils import Join
from util.parser import *
from util.hash import *

from common.singleton import Singleton

from mining.database import df

from settings import CACHE

###########################################################################################

class APP_INFOR(Singleton):

    def __init__(self):
        super().__init__()

        self.df = df.DATA_FRAME

        self._decodePath = None
        self._sha256 = None

        self._pkgName = None
        self._applicatopmActivity = None
        self.ManifestJson = None

        self.pid = None
        self.tpid = None

    def __getattr__(self, key):
        try:
            return self.__dict__[key]
        except KeyError as e:
            return None

    def parser(self, p):
        if isinstance(p, XmlParser):
            self._pkgName = p.parser('manifest', 'package')
            self._applicatopmActivity = p.parser('application', 'android:name')

            add_idx = pd.Series({'pkg': self._pkgName}).rename(self._sha256)
            self.df = self.df.append(add_idx)

            self.df.to_csv(Join(CACHE, ".data.csv"), mode='w')

        elif isinstance(p, JsonParser):
            self._ManifestJson = p.parser()

    @property
    def decodePath(self):
        return self._decodePath

    @decodePath.setter
    def decodePath(self, decodePath):
        self._decodePath = decodePath

    @property
    def sha256(self):
        return self._sha256

    @sha256.setter
    def sha256(self, sha256):
        self._sha256 = sha256

    @property
    def pkgName(self):
        return self._pkgName

    @pkgName.setter
    def pkgName(self, pkgName):
        self._pkgName = pkgName
