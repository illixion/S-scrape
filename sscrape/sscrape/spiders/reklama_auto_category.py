import scrapy


class ReklamaAutoCategorySpider(scrapy.Spider):
    name = 'reklama-auto-cat'
    allowed_domains = ['reklama.bb.lv']
    start_urls = ['https://reklama.bb.lv/lv/menus-models.html']

    def parse(self, response):
        for category in response.xpath('//td[@class="left_column"]/ul//a/text()').getall()[:-1]:
            yield {
                "category": category.strip()
            }
