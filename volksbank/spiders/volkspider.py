import scrapy
from ..items import VolksbankItem
import re

pattern = r'(\r)?(\n)?(\t)?(\xa0)?'


class VolkspiderSpider(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES': {'volksbank.pipelines.VolksbankPipeline':300},

    }
    name = 'volkspider'
    start_urls = ['https://www.volksbank-vorarlberg.at/jugend/news/']

    # base_url = 'https://www.volksbank-vorarlberg.at'

    def parse(self, response):
        articles = response.xpath('//div[@class="column col-1-1-1-1"]')
        for article in articles:
            link = article.xpath('.//h3/a/@href').get()
            yield scrapy.Request(response.urljoin(link), callback=self.parse_article)

    def parse_article(self, response):
        title = response.xpath('//div[@class="column_padding article_block"]/h1/text()').get()
        content = response.xpath(
            '//div[@class="column_padding article_block"]//text()[not (ancestor::form) and not(ancestor::font)]').getall()
        content = ' '.join([text.strip() for text in content if text.strip()])
        content = re.sub(pattern, '', content).strip()
        item = VolksbankItem()
        item['title'] = title
        item['content'] = content
        yield item
