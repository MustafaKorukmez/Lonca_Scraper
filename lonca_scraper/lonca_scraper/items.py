# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LoncaScraperItem(scrapy.Item):
    _id = scrapy.Field()
    stock_code = scrapy.Field()
    color = scrapy.Field()
    discounted_price = scrapy.Field()
    images = scrapy.Field()
    is_discounted = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    price_unit = scrapy.Field()
    product_type = scrapy.Field()
    quantity = scrapy.Field()
    sample_size = scrapy.Field()
    series = scrapy.Field()
    status = scrapy.Field()
    fabric = scrapy.Field()
    model_measurements = scrapy.Field()
    product_measurements = scrapy.Field()
    createdAt = scrapy.Field()
    updatedAt = scrapy.Field()
