# -*- coding:utf-8 -*-

#############################################################################

import os
from util.fsUtils import Join

#############################################################################

BASE_DIR        = os.path.dirname(os.path.realpath(__file__))

ELASTIC_PATH = r'C:\elasticsearch-hadoop-7.8.1\dist\elasticsearch-hadoop-7.8.1.jar'

ES_CONF = {
    "es.nodes": "127.0.0.1:9200",
    "es.nodes.discovery": "true",
    "es.update.script.inline": "ctx._source.location = params.location",
    "es.update.script.params": "location:",
    "es.write.operation": "upsert"
}

#############################################################################
