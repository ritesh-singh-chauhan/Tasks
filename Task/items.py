# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TaskItem(scrapy.Item):
    title= scrapy.Field()
    link= scrapy.Field()
    link_hash=scrapy.Field()
    description=scrapy.Field()
    pubDate=scrapy.Field()
    creator=scrapy.Field()
    content=scrapy.Field()
    media=scrapy.Field()
    updated_at=scrapy.Field()
    pass
class FullDescription(scrapy.Item):
    link_hash=scrapy.Field()
    fulldescription=scrapy.Field()
    pass
