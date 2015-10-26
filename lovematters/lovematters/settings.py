#!/usr/bin/env python
# encoding: utf-8

import sys
import os
from os.path import dirname

path = dirname(dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(path)

from misc.log import *


BOT_NAME = 'lovematters'

SPIDER_MODULES = ['lovematters.spiders']
NEWSPIDER_MODULE = 'lovematters.spiders'

ITEM_PIPELINES = {
    'lovematters.pipelines.MySQLStorePipeline',
}

LOG_LEVEL = 'INFO'

# DOWNLOAD_DELAY = .5    # 250 ms of delay
# RANDOMIZE_DOWNLOAD_DELAY = True

MAX_COMMENT_NUM = 20

MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'spider_test'
MYSQL_USER = 'root'
MYSQL_PASSWD = ''
