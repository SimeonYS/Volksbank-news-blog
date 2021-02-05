# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class VolksbankItem(scrapy.Item):
   title = scrapy.Field()
   content = scrapy.Field()

class BlogItem(scrapy.Item):
   title = scrapy.Field()
   date = scrapy.Field()
   content = scrapy.Field()