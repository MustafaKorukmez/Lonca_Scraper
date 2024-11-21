import logging
import datetime

class SpiderLogger:

    
    def __init__(self, spider_name):
        self.logger = logging.getLogger(spider_name)
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
        filename=f'logs/xml_scraper_{datetime.datetime.now().strftime("%Y%m%d")}.log',
        level=logging.INFO,
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s'
        )
        
    def error(self, message):
        self.logger.error(message)
        
    def info(self, message):
        self.logger.info(message)
        
    def debug(self, message):
        self.logger.debug(message)