import json
import scrapy
from ..items import AutoItem


class SsAutoSpider(scrapy.Spider):
    name = 'ss-auto'
    allowed_domains = ['ss.com']
    start_urls = ["https://www.ss.com/lv/transport/cars/sell/rss/"]

    def parse(self, response):
        for url in response.xpath("//channel/item/link/text()").getall():
            yield scrapy.Request(url=url, callback=self.parse_ad)

    def parse_ad(self, response):
        item = AutoItem()
        images = []

        for image in response.xpath('//img[@class="pic_thumbnail isfoto"]/@src').getall():
            images.append(
                {"title": "Image", "url": image.replace(".t.", ".800.")}
            )

        item["images"] = (json.dumps(images) or '', )
        item["thumbnail"] = (response.xpath('//img[@class="pic_thumbnail isfoto"]/@src').get() or '', )
        item["description"] = ("".join(response.xpath('//div[@id="msg_div_msg"]/text()').getall()) or '', )

        price = response.xpath('//span[@id="tdo_8"]/text()').re(r"\d+")

        item["price"] = (price[0] if len(price) > 0 else 0 or '', )
        item["year"] = (response.xpath('//td[@id="tdo_18"]/text()').get() or '', )
        item["engine"] = (response.xpath('//td[@id="tdo_15"]/text()').get() or '', )
        item["transmision"] = (response.xpath('//td[@id="tdo_35"]/text()').get() or '', )
        item["mileage"] = (response.xpath('//td[@id="tdo_16"]/text()').get() or '', )
        item["colour"] = (response.xpath('//td[@id="tdo_17"]/text()').get(),)
        item["type"] = (response.xpath('//td[@id="tdo_32"]/text()').get() or '', )
        item["technical_inspection"] = (response.xpath('//td[@id="tdo_223"]/text()').get() or '', )
        item["options_data"] = (json.dumps(response.xpath('//b[@class="auto_c"]/text()').getall()) or '', )
        item["original_url"] = (response.url or '', )
        item["contact_data"] = ("".join(response.xpath('//span[@id="phone_td_1"]/descendant-or-self::*/text()').getall()).strip() or '', )
        item["post_in_data"] = (next(iter(response.xpath('//td[@class="msg_footer" and contains(text(), "Datums")]/text()').re(r"\d+\.\d+\.\d+")), "") or '', )
        item["post_in_time"] = (next(iter(response.xpath('//td[@class="msg_footer" and contains(text(), "Datums")]/text()').re(r"\d+\:\d+")), "") or '', )
        item["subcat"] = (response.xpath('//h2[@class="headtitle"]/descendant-or-self::*/text()').getall()[2] or '', )
        item["model"] = (response.xpath('//td[@id="tdo_31"]/text()').get() or '', )
        yield item
