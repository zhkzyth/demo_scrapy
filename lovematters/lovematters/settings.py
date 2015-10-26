# Scrapy settings for lovematters project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

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
MYSQL_DBNAME = 'bra'
MYSQL_USER = 'root'
MYSQL_PASSWD = ''
