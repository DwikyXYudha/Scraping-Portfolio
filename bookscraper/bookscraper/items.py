# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscraperItem(scrapy.Item):
    pass

class BookItem(scrapy.Item):
    name = scrapy.Field()
    image = scrapy.Field()
    url = scrapy.Field()
    rating = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    num_reviews = scrapy.Field()
    category = scrapy.Field()
    product_description = scrapy.Field()
