# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TaskItem(scrapy.Item):
    title       =   scrapy.Field(type=str)
    link        =   scrapy.Field(type=str)
    link_hash   =   scrapy.Field(type=str)
    description =   scrapy.Field(type=str)
    pubDate     =   scrapy.Field(type=str)

class FullDescription(scrapy.Item):
    link_hash       =   scrapy.Field(type=str)
    fulldescription =   scrapy.Field(type=str)
