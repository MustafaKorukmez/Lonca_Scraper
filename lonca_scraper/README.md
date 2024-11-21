# Lonca Scraper - Technical Documentation
### Table of Contents
1. Project Overview
2. Installation
3. Project Structure
4. Configuration
5. Components
6. Usage
7. Development
8. Troubleshooting
9. API Reference
10. Contributing
---
## 1. Project Overview
### Introduction
Lonca Scraper is a specialized web scraping application built using the Scrapy framework. It's designed to extract product information from XML files and store the data in a MongoDB database, with sophisticated handling of product updates and new entries.
### Key Features
* XML file parsing
* MongoDB integration
* Automated product updates
* Timestamp management
* Image URL extraction
* Price conversion handling
* Color variant management
### Technologies Used
* Python 3.7+
* Scrapy Framework
* MongoDB
* PyMongo
* w3lib

## 2. Installation
### Prerequisites
* Python 3.7 or higher
* MongoDB 4.0 or higher
* pip (Python package manager)
### Setup Process
```bash
# Clone the repository
git clone https://github.com/MustafaKorukmez/lonca_scraper.git
cd lonca_scraper

# Create and activate virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```
### Configuration
```python
# settings.py configuration
BOT_NAME = "lonca_scraper"
SPIDER_MODULES = ["lonca_scraper.spiders"]
NEWSPIDER_MODULE = "lonca_scraper.spiders"
```

## 3. Project Structure

```bash
lonca_scraper/
├── lonca_scraper/
│   ├── __init__.py
│   ├── items.py           # Data structure definitions
│   ├── middlewares.py     # Middleware components
│   ├── pipelines.py       # Data processing pipelines
│   ├── settings.py        # Project settings
│   ├── spiders/
│   │   ├── __init__.py
│   │   └── lonca_spider.py # Main spider implementation
│   └── utils/
│       ├── __init__.py
│       └── utils.py       # Utility functions
│       └── logging.py     # Logging functions
│       └── validation.py # Data validation functions
└── scrapy.cfg            # Scrapy configuration file
```

## 4. Configuration
### MongoDB Settings
```python
# Pipeline MongoDB configuration
MONGODB_URI = "mongodb://localhost:27017/"
MONGODB_DATABASE = "lonca_database"
MONGODB_COLLECTION = "products"
```

### Spider Settings
```python
# Spider configuration
name = "lonca"
start_urls = ["file:file.xml file path"]
iterator = "iternodes"
itertag = "Product"
```

## 5. Components
### LoncaSpider
The main spider class responsible for parsing XML data.

```python
from scrapy.spiders import XMLFeedSpider
from lonca_scraper.items import LoncaScraperItem
from lonca_scraper.utils.utils import Utils
from bson.objectid import ObjectId
from w3lib.html import remove_tags
import re

class LoncaSpider(XMLFeedSpider):
    """
    Spider for parsing product data from XML files
    """
    name = "lonca"
    start_urls = ["file:///path/to/your/xml/file.xml"]
    iterator = "iternodes"
    itertag = "Product"

    def parse_node(self, response, node):
        # Implementation details
```

### LoncaScraperPipeline
Handles data processing and MongoDB operations

```python
from pymongo import MongoClient
from lonca_scraper.utils.utils import Utils

class LoncaScraperPipeline:
    """
    Pipeline for processing and storing scraped data
    """
    def __init__(self):
        # Setup database connection
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["lonca_database"]
        self.collection = self.db["products"]

    def process_item(self, item, spider):
        # Implementation details

    def close_spider(self, spider):
        # Close database connection
        self.client.close()
```
### Logging Class
Provides auxiliary function for logs
```python
from datetime import datetime

class SpiderLogger:
```
### Validation Class
 
Provides auxiliary function for validation
```python
class DataValidator:
```

### Utils Class
Provides utility functions for timestamp management.

```python
from datetime import datetime, timezone, timedelta

class Utils:
    """
    Utility functions for the scraper
    """
    def __init__(self):
        pass

    def get_current_time(self):
        # Implementation details
```

### LoncaScraperItem
Defines the data structure for scraped products.

```python
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
```

## 6. Usage
### Running the Spider
```bash
# Basic usage
scrapy crawl lonca

```

### Data Model

```python
class LoncaScraperItem(scrapy.Item):
    _id = Field()
    stock_code = Field()
    color = Field()
    discounted_price = Field()
    images = Field()
    # ... other fields
```

## 7. Development
### Adding New Features
1. Create a new spider class
2. Implement required methods
3. Update pipeline as needed
4. Add new fields to items.py

### Testing

```bash
# Run tests
python -m unittest discover tests

# Run specific test
python -m unittest tests.test_spider
```

## 8. Troubleshooting
### Common Issues
#### 1. MongoDB Connection Issues

```bash
# Check connection
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
client.server_info()
```

#### 2. XML Parsing Errors
* Verify XML file structure
* Check file path
* Validate XML syntax

#### 3. Pipeline Processing Issues
* Check MongoDB permissions
* Verify data types
* Review timestamp formats

## 9. API Reference
### Spider Methods

```python
def parse_node(self, response, node):
    """
    Parse individual XML nodes

    Args:
        response: Response object
        node: XML node

    Returns:
        LoncaScraperItem: Processed item
    """
```

### Pipeline Methods

```python
def process_item(self, item, spider):
    """
    Process and store items

    Args:
        item: LoncaScraperItem
        spider: Spider instance

    Returns:
        item: Processed item
    """
```

## 10. Contributing
### Guidelines
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Create a Pull Request

### Code Style
* Follow PEP 8
* Add docstrings
* Comment complex logic
* Use type hints

### Version Control

```bash
# Create new feature branch
git checkout -b feature/new-feature

# Commit changes
git commit -m "Add new feature"

# Push changes
git push origin feature/new-feature
```

### Appendix
#### A. Dependencies

```bash
scrapy>=2.5.0,<3.0.0
pymongo>=3.11.0,<4.0.0
w3lib>=1.22.0,<2.0.0
```

#### B. Configuration Options

```python
# Available settings
ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 3
```

#### C. Error Codes

```python
# Common error codes
ERROR_MONGODB_CONNECTION = 1001
ERROR_XML_PARSE = 1002
ERROR_PIPELINE_PROCESS = 1003
```

### Contact Information
For support or queries:
* Email: korukmezm@gmail.com
* GitHub: https://github.com/MustafaKorukmez