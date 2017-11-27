# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

from twisted.internet import defer, reactor
from twisted.enterprise.adbapi import ConnectionPool
import logging
import hashlib
import datetime
from cmic.settings import IMAGES_STORE


class CmicPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool
        # create table
        """
        CREATE SEQUENCE tablename_colname_seq;
        CREATE TABLE tablename (
            colname integer NOT NULL DEFAULT nextval('tablename_colname_seq')
        );
        ALTER SEQUENCE tablename_colname_seq OWNED BY tablename.colname;
        """

        # a = dbpool.runQuery("SELECT data from test WHERE id=1")
        print("db")
        # print(a[0][0])
        # a.addCallback(self.printResult)
        # a = dbpool.runInteraction(self.do_select)
        # a.addCallback(self.printResult)

    @classmethod
    def from_settings(cls, settings):

        dbparms = {
            'host': settings["DB_HOST"],
            'dbname': settings["DB_DBNAME"],
            'user': settings["DB_USER"],
            'password': settings["DB_PASSWORD"],
        }

        dbpool = ConnectionPool('psycopg2', **dbparms)

        return cls(dbpool)

    # def print_result(self, x):
    #     if x:
    #         print(x[0][0])
    #     else:
    #         print("No item")
    #
    # def do_select(self, cursor, id=0):
    #     cursor.execute("SELECT data from test WHERE id=1")
    #     return cursor.fetchall()

    # def getAge(id):
    #     return dbpool.runQuery("SELECT age FROM users WHERE name = ?", user)

    def handle_error(self, failure, item, spider):
        #处理异步插入的异常
        print(failure)

    def process_item(self, item, spider):
        # pass
        # 使用Twisted将mysql插入变成异步执行
        # runInteraction可以将传入的函数变成异步的
        logging.info('do autopadding item value')
        item['web_path_sha1'] = hashlib.sha1(item['web_path'].encode()).hexdigest()
        item['create_date'] = datetime.datetime.now()
        # item['local_path'] = IMAGES_STORE + '/full/' + item['web_path_sha1'] + '.' + item['web_path'].split('.')[-1]
        item['local_path'] = IMAGES_STORE + '/' + item['image_paths'][0]
        item['file_hash'] = item['image_paths'][0].split('/')[-1].split('.')[0]
        spider.log('Well, here is an Item: %s.' % item)
        query = self.dbpool.runInteraction(self.do_insert, item)
        # #处理异常
        query.addErrback(self.handle_error, item, spider)
        return item

    def do_insert(self, cursor, item):
        """

        :param cursor:
        :param item:
        :return:
        """
        insert_sql = """
        INSERT INTO comic_record_curhash(no,comic_id,comic_hui,comic_img_order,web_path_sha1,web_path,local_path,file_hash) VALUES (nextval('comic_seq'),%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (web_path_sha1) DO NOTHING;
        """
        cursor.execute(insert_sql, (
            item['comic_name'], item['comic_hui'], item['img_order'], item['web_path_sha1'],
            item['web_path'], item['local_path'], item['file_hash']
        ))


class CmicImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            logging.info("Downloading image_url:" + image_url)
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

