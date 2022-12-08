# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderSteamItem(scrapy.Item):
    name = scrapy.Field()
    category = scrapy.Field()
    reviews_count = scrapy.Field()
    review_points = scrapy.Field()
    realise_data = scrapy.Field()
    developer = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    platforms_available = scrapy.Field()
