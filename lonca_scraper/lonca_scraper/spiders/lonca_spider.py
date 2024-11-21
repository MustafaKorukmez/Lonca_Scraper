import scrapy
from scrapy.spiders import XMLFeedSpider
from lonca_scraper.items import LoncaScraperItem
from w3lib.html import remove_tags
import re
from pymongo import MongoClient
from bson.objectid import ObjectId
from lonca_scraper.utils.utils import Utils
from lonca_scraper.utils.logging import SpiderLogger
from lonca_scraper.utils.validation import DataValidator

class LoncaSpider(XMLFeedSpider):
    name = "lonca"
    # Local test file path - update for production
    start_urls = ["file:///C:/Users/m00878601/Desktop/Projects/Lonca/lonca-sample.xml"]
    iterator = "iternodes"
    itertag = "Product"

    def __init__(self, *args, **kwargs):
        super(XMLFeedSpider, self).__init__(*args, **kwargs)
        self.spider_logger = SpiderLogger(spider_name=self.name)
        self.data_validator = DataValidator()
        self.utils = Utils()

    def parse_node(self, response, node):
        self.spider_logger.info("Starting to parse product node")
        item = LoncaScraperItem()

        # Create unique identifier for MongoDB
        try:
            item["_id"] = ObjectId()
            self.spider_logger.debug("Created MongoDB ObjectId")
        except Exception as e:
            self.spider_logger.error(f"Failed to create ObjectId: {str(e)}")
            return None
        
        # Get basic product info
        product_id = node.xpath("@ProductId").get()
        name = node.xpath("@Name").get()
        item["name"] = name.title()
        if not item["name"]:
            self.spider_logger.error(f"Product name not found for product ID: {product_id}")

        # Product images
        images = node.xpath("Images/Image/@Path").getall()
        item["images"] = images
        if not images:
            self.spider_logger.info(f"No images found for product ID: {product_id}")

        # Parse product details section
        self.spider_logger.info("Parsing product details")
        product_details = {}
        for detail in node.xpath("ProductDetails/ProductDetail"):
            detail_name = detail.xpath("@Name").get()
            detail_value = detail.xpath("@Value").get()
            product_details[detail_name] = detail_value

        # Handle pricing info
        try:
            item["price"] = float(product_details.get("Price").replace(",", "."))
            item["discounted_price"] = float(product_details.get("DiscountedPrice").replace(",", "."))
            self.spider_logger.debug(f"Parsed prices - Regular: {item['price']}, Discounted: {item['discounted_price']}")
        except (ValueError, AttributeError) as e:
            self.spider_logger.error(f"Error parsing price values: {str(e)}")
            return None

        item["product_type"] = product_details.get("ProductType")
        item["quantity"] = int(product_details.get("Quantity"))

        # Handle color variants
        color_value = product_details.get("Color", "")
        if color_value:
            item["color"] = [color.strip() for color in color_value.split(",") if color.strip()]
            self.spider_logger.debug(f"Found colors: {item['color']}")
        else:
            item["color"] = []
            self.spider_logger.info("No color information found")

        # Build unique stock code
        try:
            item["stock_code"] = str(product_id.split("-")[0]) + "-" + str(item["color"][0])
            self.spider_logger.info(f"Generated stock code: {item['stock_code']}")
        except IndexError:
            self.spider_logger.error("Failed to generate stock code - missing color information")
            return None
        if item["discounted_price"] < item["price"] and item["discounted_price"] != 0:
            item["is_discounted"] = True
        else:
            item["is_discounted"] = False   

        # Extract product details from description
        self.spider_logger.info("Parsing product description")
        description_html = node.xpath("Description/text()").get()
        if description_html:
            description_text = remove_tags(description_html)
            description_text = description_text.replace("\n", "").replace("\t", "").strip()

            # Parse fabric details
            fabric_match = re.search(r"Kumaş Bilgisi:</strong>\s*(.*?)</li>", description_html, re.DOTALL)
            if fabric_match:
                item["fabric"] = fabric_match.group(1).strip()
                self.spider_logger.debug(f"Found fabric information: {item['fabric']}")
            else:
                self.spider_logger.info(f"Failed to receivefabric data for product with stock code{item["stock_code"]}")
                
            # Look for model measurements
            model_measurements_match = re.search(r"Model Ölçüleri:</strong>\s*(.*?)</li>", description_html, re.DOTALL)
            if model_measurements_match:
                item["model_measurements"] = model_measurements_match.group(1).strip().replace("&nbsp;", "")

            # Look for product measurements
            product_measurements_match = re.search(r"Ürün Ölçüleri:</strong>\s*(.*?)</li>", description_html, re.DOTALL)
            if product_measurements_match:
                item["product_measurements"] = product_measurements_match.group(1).strip()

            # Look for sample size info
            sample_size_match = re.search(r"Modelin üzerindeki ürün <strong>\s*(.*?)</strong>", description_html, re.DOTALL)
            if sample_size_match:
                item["sample_size"] = sample_size_match.group(1).strip()

        # Set default fields
        item["price_unit"] = "USD"
        
        if item["quantity"] == 0:
            item["status"] = "Active"
        else:
            item["status"] = "Passive"

        # Set timestamps
        now_with_custom_offset = Utils.get_current_time(self)
        item["createdAt"] = now_with_custom_offset
        item["updatedAt"] = now_with_custom_offset

        # Veriyi doğrula
        if not self.data_validator.is_valid_product(item):
            self.spider_logger.error(f"Validation failed for node: {item['stock_code']}")
            return None

        yield item