import json
import scrapy
from bs4 import BeautifulSoup
from datetime import datetime
from ..items import AutoItem


class VissAutoSpider(scrapy.Spider):
    name = 'viss-auto'
    allowed_domains = ['viss.lv']
    start_urls = ["http://viss.lv/lv/sludinajumi/c/13/"]

    def parse(self, response):
        for url in response.xpath('//table[@class="slud_saraksta_tabula"]//a/@href').getall():
            yield scrapy.Request(url="http://viss.lv" + url, callback=self.parse_ad)

    def parse_ad(self, response):
        page_html = BeautifulSoup(response.text, "html.parser")
        result = self.parse_viss_auto(page_html)

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

    def parse_viss_auto(self, page_html):
        images = []
        try:
            for image in page_html.findAll("img", {"class": "maza_bilde"}):
                images.append(
                    {"title": "Image", "url": "http://viss.lv" + image["src"]}
                )
        except:
            pass

        infotable = {
            "Auto marka:": "",
            "Izlaiduma gads:": "",
            "Motora tilpums:": "",
            "Degvielas veids:": "",
            "Atrumkārba:": "",
            "Nobraukums (km):": "",
            "Krāsa:": "",
            "Virsbūves tips:": "",
        }
        for table in page_html.findAll("table", {"class": "ad_view_user_text"}):
            for row in table.findAll("tr"):
                col = row.findAll("td")
                try:
                    infotable[col[0].text] = col[1].text
                except IndexError:
                    pass

        try:
            result_object = {
                "thumbnail": "",
                "description": "",
                "images": "",
                "price": "0",
                "year": "0",
                "engine": "",
                "transmision": "",
                "mileage": "0",
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
                f"Error while parsing C-data in , viss might've changed format: {e}"
            )
            return None

        try:
            result_object["price"] = "".join(
                i for i in infotable["Cena:"].split(".")[0] if i.isdigit()
            )
        except:
            pass
        try:
            result_object["thumbnail"] = images[0]["url"]
        except:
            pass
        try:
            result_object["description"] = infotable["Teksts:"]
        except:
            pass
        try:
            result_object["contact_data"] = "".join(
                i for i in infotable["Telefons:"] if i.isdigit()
            )
        except:
            pass
        try:
            result_object["images"] = json.dumps(images)
        except:
            pass
        try:
            result_object["year"] = infotable["Izlaiduma gads:"].strip()
        except:
            pass
        try:
            result_object["engine"] = infotable["Degvielas veids:"].strip()
        except:
            pass
        try:
            result_object["transmision"] = infotable["Atrumkārba:"].strip()
        except:
            pass
        try:
            result_object["mileage"] = infotable["Nobraukums (km):"].strip()
        except:
            pass
        try:
            result_object["colour"] = infotable["Krāsa:"].strip()
        except:
            pass
        try:
            result_object["type"] = infotable["Virsbūves tips:"].strip()
        except:
            pass
        try:
            result_object["subcat"] = infotable["Auto marka:"].strip()
        except:
            pass

        return result_object
