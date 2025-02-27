# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 爬虫获取到的数据需要组装成item对象
class ScrapyLearnItem(scrapy.Item):
    # define the fields for your item here like:
    position = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()


class SimpleWallpaperItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
