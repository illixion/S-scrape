import json
import scrapy
from bs4 import BeautifulSoup
from datetime import datetime
from ..items import AutoItem


class MmAutoSpider(scrapy.Spider):
    name = 'mmlv-auto'
    allowed_domains = ['mm.lv', "im.mm.lv"]
    start_urls = ["https://mm.lv/vieglie-auto"]

    def parse(self, response):
        for url in response.xpath('//*[@id="listing-card-list"]/li[contains(@class, "listing-card")]//a/@href').getall():
            yield scrapy.Request(url=url, callback=self.parse_ad)

    def parse_ad(self, response):
        page_html = BeautifulSoup(response.text, "html.parser")
        result = self.parse_mm_auto(page_html, response)

        item = AutoItem()
        item["images"] = result["images"],
        item["thumbnail"] = result["thumbnail"],
        item["description"] = result["description"],
        item["price"] = result["price"],
        item["year"] = result["year"],
        item["engine"] = result["engine"],
        item["transmision"] = result["transmision"],
        item["mileage"] = result["mileage"],
        item["colour"] = result["colour"],
        item["type"] = result["type"],
        item["technical_inspection"] = result["technical_inspection"],
        item["options_data"] = result["options_data"],
        item["original_url"] = response.url,
        item["contact_data"] = result["contact_data"],
        item["post_in_data"] = result["post_in_data"],
        item["post_in_time"] = result["post_in_time"],
        item["subcat"] = result["subcat"],
        item["model"] = result["model"],
        item["main_data"] = result["main_data"],
        yield item

    def parse_mm_auto(self, page_html, response):
        images = []
        try:
            for image in page_html.select(".rsTmb"):
                images.append({"title": "Image", "url": image["src"]})
        except:
            pass

        table_elements = response.xpath('//div[@class="item-block second-item-block item-description"]//ul[@class="ad-detail-info"]//li//text()').getall()
        try:
            table_elements.remove("Galvenās iezīmes")
        except ValueError:
            pass

        # Unstable, will probably break in the future
        infotable = {}
        for idx, val in enumerate(table_elements):
            if idx % 2 == 0:
                infotable[val] = ""
            else:
                infotable[table_elements[idx - 1]] = val

        result_object = {
            "thumbnail": "",
            "description": "",
            "images": "",
            "price": "0",
            "year": "",
            "engine": "",
            "transmision": "",
            "mileage": "",
            "colour": "",
            "type": "",
            "technical_inspection": "",
            "main_data": "",
            "options_data": "",
            "original_url": "",
            "contact_data": "",
            "post_in_data": datetime.now().strftime("%d.%m.%Y"),
            "post_in_time": datetime.now().strftime("%H:%M"),
            "subcat": "Cits",
            "model": "",
        }

        try:
            result_object["price"] = "".join(
                i for i in page_html.select_one(".currency-value").text if i.isdigit()
            )
        except:
            pass
        try:
            result_object["thumbnail"] = images[0]["url"]
        except:
            pass
        try:
            result_object["description"] = page_html.select_one(".item_osc_desc").text
        except:
            pass
        # try:
        #     result_object["contact_data"] = "".join(
        #         i
        #         for i in page_html.select_one(".tel_number").find("span").text
        #         if i.isdigit()
        #     )
        # except:
        #     pass
        try:
            result_object["images"] = json.dumps(images)
        except:
            pass
        try:
            result_object["year"] = infotable["Izlaiduma gads"].split("/")[0]
        except:
            pass
        try:
            result_object["engine"] = infotable[" Dzinējs"]
        except:
            pass
        try:
            result_object["transmision"] = infotable["Ātrumkārba"]
        except:
            pass
        try:
            result_object["mileage"] = infotable["Noskrējiens"]
        except:
            pass
        try:
            result_object["colour"] = infotable["Krāsa"]
        except:
            pass
        try:
            result_object["type"] = infotable["Virsbūves tips"]
        except:
            pass
        try:
            result_object["technical_inspection"] = infotable["Tehniskā apskate"]
        except:
            pass
        try:
            result_object["subcat"] = (
                page_html.select_one(".breadcrumb").find("li", {"class": "penult"}).text
            )
        except:
            pass

        return result_object
