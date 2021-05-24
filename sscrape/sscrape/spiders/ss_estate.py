import json
from json import dumps
import scrapy
from ..items import EstateItem


class SsEstateSpider(scrapy.Spider):
    name = 'ss-estate'
    allowed_domains = ['ss.com']
    start_urls = ["https://www.ss.com/lv/real-estate/sell/rss/"]

    def parse(self, response):
        for url in response.xpath("//channel/item/link/text()").getall():
            yield scrapy.Request(url=url, callback=self.parse_ad)

    def parse_ad(self, response):
        item = EstateItem()
        images = []

        for image in response.xpath('//img[@class="pic_thumbnail isfoto"]/@src').getall():
            images.append(
                {"title": "Image", "url": image.replace(".t.", ".800.")}
            )

        item["images"] = (json.dumps(images) or '', )
        item["thumbnail"] = (response.xpath('//img[@class="pic_thumbnail isfoto"]/@src').get() or '', )
        item["description"] = ("".join(response.xpath('//div[@id="msg_div_msg"]/text()').getall()) or '', )

        price_re = response.xpath('//*[@id="tdo_8"]/text()').re(r"^.+?(?=\€)")
        if len(price_re) != 0:
            price = "".join(
                i for i in response.xpath('//*[@id="tdo_8"]/text()').re(r"^.+?(?=\€)")[0] if i.isdigit()
            )
        else:
            price = 0
        item["price"] = (str(price), )

        location_other = response.xpath('//td[@id="tdo_1284"]/text()').get()
        if location_other is not None:
            try:
                item["city"] = (location_other.strip().split(", ")[0] or '', )
            except:
                pass
            try:
                item["district"] = (location_other.strip().split(", ")[1] or '', )
            except:
                pass
            try:
                item["street"] = (location_other.strip().split(", ")[2] or '', )
            except:
                pass
        else:
            item["city"] = (response.xpath('//td[@id="tdo_20"]/b/text()').get() or '', )
            item["district"] = (response.xpath('//td[@id="tdo_856"]/b/text()').get() or '', )
            item["street"] = (response.xpath('//td[@id="tdo_11"]/b/text()').get() or '', )

        item["rooms"] = (response.xpath('//td[@id="tdo_1"]/text()').get() or '', )
        item["area_m2"] = (response.xpath('//td[@id="tdo_3"]/text()').get() or '', )
        item["floor"] = (response.xpath('//td[@id="tdo_4"]/text()').get() or '', )
        item["estate_series"] = (response.xpath('//td[@id="tdo_6"]/text()').get() or '', )
        item["estate_type"] = (response.xpath('//td[@id="tdo_2"]/text()').get() or '', )
        item["cadastre_number"] = (response.xpath('//td[@id="tdo_1631"]/text()').get() or '', )
        item["amenities"] = (response.xpath('//td[@id="tdo_1734"]/text()').get() or '', )
        item["contact_data"] = ("".join(response.xpath('//span[@id="phone_td_1"]/descendant-or-self::*/text()').getall()).strip() or '', )
        item["original_url"] = (response.url or '', )
        item["post_in_data"] = (next(iter(response.xpath('//td[@class="msg_footer" and contains(text(), "Datums")]/text()').re(r"\d+\.\d+\.\d+")), "") or '', )
        item["post_in_time"] = (next(iter(response.xpath('//td[@class="msg_footer" and contains(text(), "Datums")]/text()').re(r"\d+\:\d+")), "") or '', )
        yield item
