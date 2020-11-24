import scrapy


class SsAutoCategorySpider(scrapy.Spider):
    name = 'autoss-auto-cat'
    allowed_domains = ['autoss.eu']
    start_urls = ['http://www.autoss.eu/']

    def parse(self, response):
        for category in response.xpath('//select[@id="make"]/option/text()').getall()[1:]:
            yield {
                "category": category
            }
