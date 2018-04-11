import scrapy
from scrapy import Request

from college_crawler.items import CollegeCrawlerItem


class GaoKaoSpider(scrapy.Spider):
    name = "gaokao"
    allowed_domains = ["gaokao.com"]
    start_urls = [
        'http://www.gaokao.com/zhejiang/ebdx/',
        'http://www.gaokao.com/jiangsu/ebdx/'
    ]

    def parse(self, response):
        for sel in response.xpath('//div[@class="dxmd-item"]//td//a'):
            item = CollegeCrawlerItem()
            item['name'] = sel.xpath('./text()').extract_first().strip()
            item['url'] = sel.xpath('./@href').extract_first()
            yield Request(item['url'], meta={'item': item}, callback=self.parseTel)

    def parseTel(self, response):
        item = response.meta['item']
        tel = response.xpath('//ul[@class="left contact"]//p/text()').extract()[1].strip()
        item['tel'] = tel
        yield item
