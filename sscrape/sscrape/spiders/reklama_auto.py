import json
import scrapy
from bs4 import BeautifulSoup
from datetime import datetime
from ..items import AutoItem


class ReklamaAutoSpider(scrapy.Spider):
    name = 'reklama-auto'
    allowed_domains = ['reklama.bb.lv']
    start_urls = ["https://reklama.bb.lv/lv/transport/cars/sell/table.html?rss"]

    def parse(self, response):
        for url in response.xpath("//channel/item/link/text()").getall():
            yield scrapy.Request(url=url, callback=self.parse_ad)

    def parse_ad(self, response):
        page_html = BeautifulSoup(response.text, "html.parser")
        result = self.parse_reklama_auto(page_html)

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

    def parse_reklama_auto(self, page_html):
        images = []

        try:
            for image in page_html.select_one(".coda-nav").findAll("img"):
                images.append({"title": "Image", "url": image["data-src"]})
        except:
            pass
        infotable = {
            "Operācija": "",
            "Marka": "",
            "Modelis": "",
            "Krāsa": "",
            "Virsbūve": "",
            "Cena": "",
            "Pārnesumkārba:": "",
            "Durvju skaits": "",
            "Valsts numura zime": "",
            "Gads": "",
            "Nobraukums": "",
            "Dzin.": "",
        }
        for table in page_html.findAll("table", {"id": "details"}):
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
                f"Error while parsing C-data in , reklama might've changed format: {e}"
            )
            return None

        try:
            result_object["price"] = "".join(
                i for i in infotable["Cena\n\n\nEUR\nLVL\nUSD\n\n"] if i.isdigit()
            )
        except:
            pass
        try:
            result_object["thumbnail"] = images[0]["url"]
        except:
            pass
        try:
            result_object["description"] = page_html.select_one("#content").text
        except:
            pass
        try:
            result_object["contact_data"] = "".join(
                i
                for i in page_html.select_one(".tel_number").find("span").text
                if i.isdigit()
            )
        except:
            pass
        try:
            result_object["images"] = json.dumps(images)
        except:
            pass
        try:
            result_object["year"] = infotable["Gads"]
        except:
            pass
        try:
            result_object["engine"] = infotable["Dzin."]
        except:
            pass
        try:
            result_object["transmision"] = infotable["Pārnesumkārba:"]
        except:
            pass
        try:
            result_object["mileage"] = infotable["Nobraukums"]
        except:
            pass
        try:
            result_object["colour"] = infotable["Krāsa"]
        except:
            pass
        try:
            result_object["type"] = infotable["Virsbūve"]
        except:
            pass
        try:
            result_object["subcat"] = infotable["Marka"]
        except:
            pass

        return result_object
