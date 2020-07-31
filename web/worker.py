# -*- coding:utf-8 -*-

##################################################################################################

from flask_executor import Executor

##################################################################################################

executor = Executor()

def setup(app):
    app.config['EXECUTOR_TYPE'] = 'thread'  # 'process'
    app.config['EXECUTOR_MAX_WORKERS'] = 5

    executor.init_app(app)

##################################################################################################
