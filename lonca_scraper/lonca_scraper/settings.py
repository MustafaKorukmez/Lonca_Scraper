BOT_NAME = "lonca_scraper"

SPIDER_MODULES = ["lonca_scraper.spiders"]
NEWSPIDER_MODULE = "lonca_scraper.spiders"

# Core settings
ROBOTSTXT_OBEY = True

# Database pipeline configuration
ITEM_PIPELINES = {
    "lonca_scraper.pipelines.LoncaScraperPipeline": 300,
}

# System compatibility settings
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"