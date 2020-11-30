import scrapy


class VissAutoCategorySpider(scrapy.Spider):
    name = 'viss-auto-cat'
    allowed_domains = ['viss.lv']
    start_urls = ['http://viss.lv/lv/sludinajumi/c/13/']

    def parse(self, response):
        for category in response.xpath('//table[@class="filtru_tabula"]//a[@class="filtra_links"]/text()').getall():
            yield {
                "category": category
            }
