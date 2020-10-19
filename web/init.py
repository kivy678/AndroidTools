# -*- coding:utf-8 -*-

###########################################################################################

from module.database import *

###########################################################################################

def setup():
    df_dev.setup()
    df_lib.setup()
    df_dev_lib.setup()
    df_app.setup()
    df_unity.setup()
    df_il2cpp.setup()
    df_opcode.setup()
