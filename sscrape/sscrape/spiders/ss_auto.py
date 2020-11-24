import json
import scrapy
from ..items import AutoItem


class SsAutoSpider(scrapy.Spider):
    name = 'ss-auto'
    allowed_domains = ['ss.com']


def start_requests(self):
    response = scrapy.Request(url="https://www.ss.com/lv/transport/cars/sell/rss/")
    for url in response.xpath("//channel/item/link/text()").getall():
        yield scrapy.Request(url=url, callback=self.parse_url)


def parse_url(self, response):
    item = AutoItem()
    item["images"] = []

    for image in response.xpath('//img[@class="pic_thumbnail isfoto"]/@src').getall():
        item["images"].append(
            {"title": "Image", "url": image.replace(".t.", ".800.")}
        )

    item["thumbnail"] = response.xpath('//img[@class="pic_thumbnail isfoto"]/@src').get()
    item["description"] = "".join(response.xpath('//div[@id="msg_div_msg"]/text()').getall())

    price = response.xpath('//span[@id="tdo_8"]/text()').re(r"\d+")

    item["price"] = price[0] if len(price) > 0 else 0
    item["year"] = response.xpath('//td[@id="tdo_18"]/text()').get()
    item["engine"] = response.xpath('//td[@id="tdo_15"]/text()').get()
    item["transmision"] = response.xpath('//td[@id="tdo_35"]/text()').get()
    item["mileage"] = response.xpath('//td[@id="tdo_16"]/text()').get()
    item["colour"] = response.xpath('//td[@id="tdo_17"]/text()').get()
    item["type"] = response.xpath('//td[@id="tdo_32"]/text()').get()
    item["technical_inspection"] = response.xpath('//td[@id="tdo_223"]/text()').get()
    item["options_data"] = response.xpath('//b[@class="auto_c"]/text()').getall()
    item["original_url"] = response.url
    item["contact_data"] = "".join(response.xpath('//span[@id="phone_td_1"]/descendant-or-self::*/text()').getall()).strip()
    item["post_in_data"] = next(iter(response.xpath('//td[@class="msg_footer" and contains(text(), "Datums")]/text()').re(r"\d+\.\d+\.\d+")), "")
    item["post_in_time"] = next(iter(response.xpath('//td[@class="msg_footer" and contains(text(), "Datums")]/text()').re(r"\d+\:\d+")), "")
    item["subcat"] = response.xpath('//h2[@class="headtitle"]/descendant-or-self::*/text()').getall()[2]
    item["model"] = response.xpath('//td[@id="tdo_31"]/text()').get()
    item["main_data"] = json.dumps(item)
    yield item
