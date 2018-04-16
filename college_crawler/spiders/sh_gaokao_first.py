import scrapy
from scrapy import Request

from college_crawler.items import CollegeCrawlerItem


class ShangHaiGaoKaoFirstSpider(scrapy.Spider):
    name = "shanghai-gaokao-first"
    allowed_domains = ["sh.gaokao.com"]
    start_urls = [
        'http://sh.gaokao.com/shgx/shfd/'
    ]

    def parse(self, response):
        for sel in response.xpath('//div[@id="xsc_info"]//li'):
            item = CollegeCrawlerItem()
            item['name'] = sel.xpath('./a/text()').extract_first().strip()
            item['url'] = sel.xpath('./a/@href').extract_first()
            yield Request(item['url'], meta={'item': item}, callback=self.parseTel)

    def parseTel(self, response):
        item = response.meta['item']
        tel = response.xpath('//div[@class="main04"]/dl[3]/dt/text()').extract_first().strip()
        item['tel'] = tel
        yield item
