# -*- coding:utf-8 -*-

###########################################################################################

import configparser

from common import getSharedPreferences
from settings import GLOBAL_SETTINGS, SHARED_PATH

from mining.database.dataframe import DATAFRAME

###########################################################################################

def AndroidBase():
    config = configparser.ConfigParser()
    config.read(GLOBAL_SETTINGS)

    sp = getSharedPreferences(SHARED_PATH)

    edit = sp.edit()
    edit.putString('WORKING_DIR', config.get('DEFAULT', 'WORKING_DIR'))
    edit.commit()

    df = DATAFRAME.instance()
    ### init DF ###

    print("Android Config Setting Done...")