# -*- coding:utf-8 -*-

###########################################################################################

import configparser

from common import getSharedPreferences
from webConfig import GLOBAL_SETTINGS, SHARED_PATH

from module.database import *


###########################################################################################

def setup():
    config = configparser.ConfigParser()
    config.read(GLOBAL_SETTINGS)

    sp = getSharedPreferences(SHARED_PATH)

    edit = sp.edit()
    edit.putString('WORKING_DIR', config.get('DEFAULT', 'WORKING_DIR'))
    edit.commit()

    df_dev.setup()
    df_app.setup()
