import json
import scrapy
from ..items import AutoItem


class SsAutoSpider(scrapy.Spider):
    name = 'ss-estate'
    allowed_domains = ['ss.com']


def start_requests(self):
    response = scrapy.Request(url="https://www.ss.com/lv/real-estate/sell/rss/")
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

    price = response.xpath('//span[@id="tdo_8"]/text()').re(r"[\d ]+€ ")

    item["price"] = price[0] if len(price) > 0 else 0
    item["city"] = response.xpath('//td[@id="tdo_20"]/b/text()').get()
    item["district"] = response.xpath('//td[@id="tdo_856"]/b/text()').get()
    item["street"] = response.xpath('//td[@id="tdo_11"]/b/text()').get()
    item["rooms"] = response.xpath('//td[@id="tdo_1"]/text()').get()
    item["area_m2"] = response.xpath('//td[@id="tdo_3"]/text()').get()
    item["floor"] = response.xpath('//td[@id="tdo_4"]/text()').get()
    item["estate_series"] = response.xpath('//td[@id="tdo_6"]/text()').get()
    item["estate_type"] = response.xpath('//td[@id="tdo_2"]/text()').get()
    item["cadastre_number"] = response.xpath('//td[@id="tdo_1631"]/text()').get()
    item["amenities"] = response.xpath('//td[@id="tdo_1734"]/text()').get()
    item["contact_data"] = "".join(response.xpath('//span[@id="phone_td_1"]/descendant-or-self::*/text()').getall()).strip()
    item["original_url"] = response.url
    item["post_in_data"] = next(iter(response.xpath('//td[@class="msg_footer" and contains(text(), "Datums")]/text()').re(r"\d+\.\d+\.\d+")), "")
    item["post_in_time"] = next(iter(response.xpath('//td[@class="msg_footer" and contains(text(), "Datums")]/text()').re(r"\d+\:\d+")), "")
    item["main_data"] = json.dumps(item)
    yield item
