# -*- coding: utf-8 -*-
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ToscrapeBookPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    # 采用同步的机制写入mysql
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'scrapy_db', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into books(name, price, stock, upc,review_num) VALUES (%s, %s, %s, %s,%s)
        """
        self.cursor.execute(insert_sql, (item["name"], item["price"], item["stock"], item["upc"], item["review_num"]))
        self.conn.commit()


 # 异步执行
class MysqlTwistedPipeline(object):

    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 改变sql插入为异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
    #     query.addErrback(self.handle_error)
    #
    # def handle_error(self, failuer):
    #     #处理报错
    #     print(failuer)

    def do_insert(self, cursor, item):
        # 具体的插入语句

        insert_sql = """
            insert into books(name, price, stock, upc,review_num) VALUES (%s, %s, %s, %s,%s)
            """
        cursor.execute(insert_sql, (item["name"], item["price"], item["stock"], item["upc"], item["review_num"]))

