from pymongo import MongoClient
from lonca_scraper.utils.utils import Utils

class LoncaScraperPipeline:
    def __init__(self):
        # Setup database connection
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["lonca_database"]
        self.collection = self.db["products"]

    def process_item(self, item, spider):
        now_with_custom_offset = Utils.get_current_time(self)

        # Look for existing product
        existing_product = self.collection.find_one({"stock_code": item["stock_code"]})

        if existing_product:
            # Keep original creation date and ID when updating
            item["createdAt"] = existing_product["createdAt"]
            item["_id"] = existing_product["_id"]
            self.collection.replace_one({"_id": existing_product["_id"]}, dict(item))
        else:
            # Add new product
            item["createdAt"] = now_with_custom_offset
            self.collection.insert_one(dict(item))

        item["updatedAt"] = now_with_custom_offset
        return item

    def close_spider(self, spider):
        # Clean up database connection
        self.client.close()