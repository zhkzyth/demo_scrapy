#!/usr/bin/env python
# encoding: utf-8
import time
from hashlib import md5

# TODO custom log module
from scrapy import log
from scrapy.exceptions import DropItem
from scrapy import signals
from twisted.enterprise import adbapi


class MySQLStorePipeline(object):
    """A pipeline to store the item in a MySQL database.

    This implementation uses Twisted's asynchronous database API.
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    # @classmethod
    # def from_crawler(cls, crawler):

    #     pipeline = cls()
    #     crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
    #     crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)

    #     return pipeline

    def spider_opened(self, spider):
        pass

    def spider_closed(self, spider):
        pass

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        # run db query in the thread pool
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d

    def _do_upsert(self, conn, item, spider):
        """Perform an insert or update."""
        guid = self._get_guid(item)
        now = int(time.time())

        conn.execute("""SELECT EXISTS(
            SELECT 1 FROM pgc_data WHERE source_signature = %s
        )""", (guid, ))
        ret = conn.fetchone()[0]

        conn.execute("""
        SELECT id FROM pgc_source_type WHERE type = %s and name = %s
        """, (u"国内网站", u"lovematters"))

        source_type_row = conn.fetchone()
        source_type = 0
        if source_type_row:
            source_type = source_type_row[0]

        if ret:
            spider.log("repeated Item, no need to update in db: %s %r" % (guid, item))
        else:
            conn.execute("""
                INSERT INTO pgc_data (source_signature, title, content, comment, author, source_url, source_type, source_created, view_num, like_num, forward_num, play_num, comment_num, created, updated)
                VALUES (%s, %s, %s, %s, %s,  %s,%s,%s,%s,%s, %s,%s,%s,%s,%s)
            """, (guid, item['title'], item['content'], item['comment'], item['author'], item['source_url'],  source_type, item['source_created'], item['view_num'], item['like_num'], item['forward_num'], item['play_num'], item['comment_num'], now, now))
            spider.log("Item stored in db: %s %r" % (guid, item))

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        log.err(failure)

    def _get_guid(self, item):
        """Generates an unique identifier for a given item."""
        # hash based solely in the title and author field
        return md5(item['title'].encode('utf8') + item['author'].encode('utf8')).hexdigest()
