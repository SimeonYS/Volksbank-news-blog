import scrapy
from ..items import BlogItem
import re
pattern = r'(\r)?(\n)?(\t)?(\xa0)?'

class BlogspiderSpider(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES': {'volksbank.pipelines.BlogspiderPipeline':350},
    }
    name = 'blogspider'
    allowed_domains = []
    start_urls = ['https://blog.volksbank.at/']

    def parse(self, response):
        categories = response.xpath('//ul[@id="main-mobile-menu"]/li[contains(@id,"menu-item")]/a/@href').getall()
        for cat in categories:
            yield response.follow(cat, self.parse_category)
    def parse_category(self, response):

        links = response.xpath('//div[@class="list-post-body"]/h2/a/@href').getall()
        for link in links:
            yield response.follow(link, self.parse_article)

        next_page = response.xpath('//a[@class="next page-numbers"]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse_category)

    def parse_article(self, response):
       title = response.xpath('//div[@class="post-entry shortcode-content"]/h1/text()').get()
       date = response.xpath('//span[@class="post-time"]/text()').get()
       content = response.xpath('//div[@class="article-content"]//text()').getall()
       content = ' '.join([text.strip() for text in content if text.strip()])
       content = re.sub(pattern, '', content).strip()

       item = BlogItem()
       item['title'] = title
       item['date'] = date
       item['content'] = content

       yield item
