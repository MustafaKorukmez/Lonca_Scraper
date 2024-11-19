# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class LoncaScraperPipeline:

    def __init__(self):
        self.mongo_uri = 'mongodb://localhost:27017'
        self.mongo_db = 'lonca_database'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        collection_name = 'products'
        self.db[collection_name].insert_one(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
