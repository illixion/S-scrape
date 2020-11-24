import scrapy


class SsAutoCategorySpider(scrapy.Spider):
    name = 'ss-auto-cat'
    allowed_domains = ['ss.com']
    start_urls = ['https://www.ss.com/lv/transport/cars/']

    def parse(self, response):
        for category in response.css(".a_category::text").getall():
            yield {
                "category": category
            }
