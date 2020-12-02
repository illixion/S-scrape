import json
import scrapy
from bs4 import BeautifulSoup
from datetime import datetime
from ..items import AutoItem


class ELotsAutoSpider(scrapy.Spider):
    name = 'elots-auto'
    allowed_domains = ['e-lots.lv']
    start_urls = ["https://e-lots.lv/category/automobili"]

    def parse(self, response):
        for url in response.xpath('//*[@id="postsList"]//a[not(contains(@href,"search"))]/@href').getall():
            yield scrapy.Request(url=url, callback=self.parse_ad)

    def parse_ad(self, response):
        page_html = BeautifulSoup(response.text, "html.parser")
        result = self.parse_elots_auto(page_html)

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

    def parse_elots_auto(self, page_html):
        images = []
        try:
            for image in page_html.select_one(".bxslider").findAll("img", {"class": "bxslider"}):
                images.append(
                    {"title": "Image", "url": image["src"]}
                )
        except:
            pass
        infotable = {
            "Automašīnas zīmols": "",
            "Modelis": "",
            "Reģistrācijas gads": "",
            "Degvielas tips": "",
            "Pārnesumu kārba": "",
            "Stāvoklis": "",
            "Nobraukums": "",
        }
        for row in page_html.select_one("#cfContainer").findAll("div", {"class": "rounded-small"}):
            try:
                infotable[row.select_one('.detail-line-label').text] = row.select_one('.detail-line-value').text
            except:
                pass

        try:
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
        except AttributeError as e:
            print(
                f"Error while parsing C-data in , e-lots might've changed format: {e}"
            )
            return None

        try:
            price = "".join(i for i in page_html.select_one(".pricetag").text.strip().split(".")[0] if i.isdigit())
            if price != '':
                result_object["price"] = price
        except:
            pass
        try:
            result_object["thumbnail"] = images[0]["url"]
        except:
            pass
        try:
            result_object["description"] = page_html.select_one(".detail-line-content").text.strip()
        except:
            pass
        try:
            result_object["contact_data"] = "".join(
                i for i in page_html.select_one(".phoneBlock").text if i.isdigit()
            )
        except:
            pass
        try:
            result_object["images"] = json.dumps(images)
        except:
            pass
        try:
            result_object["engine"] = infotable["Degvielas tips"].strip()
        except:
            pass
        try:
            result_object["transmision"] = infotable["Pārnesumu kārba"].strip()
        except:
            pass
        try:
            result_object["mileage"] = infotable["Nobraukums"].strip()
        except:
            pass
        try:
            result_object["subcat"] = infotable["Automašīnas zīmols"].strip()
        except:
            pass

        return result_object
