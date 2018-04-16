import scrapy
from scrapy import Request

from college_crawler.items import CollegeCrawlerItem


class ShangHaiGaoKaoSecondSpider(scrapy.Spider):
    name = "shanghai-gaokao-second"
    allowed_domains = ["sh.gaokao.com"]
    start_urls = [
        'http://sh.gaokao.com/shgx/shsf/'
    ]

    def parse(self, response):
        for sel in response.xpath('//div[@id="enschool"]//li'):
            item = CollegeCrawlerItem()
            item['name'] = sel.xpath('./a/text()').extract_first().strip()
            item['url'] = sel.xpath('./a/@href').extract_first()
            yield Request(item['url'], meta={'item': item}, callback=self.parseTel)

    def parseTel(self, response):
        item = response.meta['item']
        tel = response.xpath('//div[@class="main04"]/dl[3]/dt/text()').extract_first().strip()
        item['tel'] = tel
        yield item
