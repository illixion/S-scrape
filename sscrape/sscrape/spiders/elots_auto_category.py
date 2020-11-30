import scrapy


class ELotsAutoCategorySpider(scrapy.Spider):
    name = 'elots-auto-cat'
    allowed_domains = ['e-lots.lv']
    start_urls = ['https://e-lots.lv/category/automobili']

    def parse(self, response):
        for category in response.xpath('//select[@id="cf.25"]/option/text()').getall()[1:]:
            yield {
                "category": category.strip()
            }
