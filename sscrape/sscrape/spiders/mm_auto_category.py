import scrapy


class MmAutoCategorySpider(scrapy.Spider):
    name = 'mm-auto-cat'
    allowed_domains = ['mm.lv']
    start_urls = ['https://mm.lv/vieglie-auto']

    def parse(self, response):
        for category in response.xpath('//div[@class="search-cat-list colp3 colm2"]//a[@class="subcat c_2"]/text()').getall():
            yield {
                "category": category
            }
