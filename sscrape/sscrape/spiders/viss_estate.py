import json
import scrapy
from bs4 import BeautifulSoup
from datetime import datetime
from ..items import EstateItem


class VissEstateSpider(scrapy.Spider):
    name = 'viss-estate'
    allowed_domains = ['viss.lv']
    start_urls = ["http://viss.lv/sludinajumi/c/24/"]

    def parse(self, response):
        for url in response.xpath('//table[@class="slud_saraksta_tabula"]//a/@href').getall():
            yield scrapy.Request(url="http://viss.lv" + url, callback=self.parse_ad)

    def parse_ad(self, response):
        page_html = BeautifulSoup(response.text, "html.parser")
        result = self.parse_viss_estate(page_html)

        item = EstateItem()
        item["images"] = result["images"],
        item["thumbnail"] = result["thumbnail"],
        item["description"] = result["description"],
        item["price"] = result["price"],
        item["city"] = result["city"],
        item["district"] = result["district"],
        item["street"] = result["street"],
        item["rooms"] = result["rooms"],
        item["area_m2"] = result["area_m2"],
        item["floor"] = result["floor"],
        item["estate_series"] = result["estate_series"],
        item["estate_type"] = result["estate_type"],
        item["cadastre_number"] = result["cadastre_number"],
        item["amenities"] = result["amenities"],
        item["contact_data"] = result["contact_data"],
        item["original_url"] = response.url,
        item["post_in_data"] = result["post_in_data"],
        item["post_in_time"] = result["post_in_time"],
        item["main_data"] = result["main_data"],
        yield item

    def parse_viss_estate(self, page_html):
        images = []
        try:
            for image in page_html.findAll("img", {"class": "maza_bilde"}):
                images.append(
                    {"title": "Image", "url": "http://viss.lv" + image["src"]}
                )
        except:
            pass

        infotable = {
            "Vieta:": "",
            "Iela:": "",
            "Istabas:": "",
            "Platība (m2):": "",
            "Stāvs:": "",
            "Sērija:": "",
            "Mājas tips:": "",
            "Ērtības:": "",
            "Apkure:": "",
            "Cena:": "",
            "Teksts:": "",
            "Kontakti:": "",
            "Pievienots:": "",
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
                "city": "0",
                "district": "",
                "street": "",
                "rooms": "0",
                "area_m2": "",
                "floor": "",
                "estate_series": "",
                "estate_type": "",
                "cadastre_number": "",
                "amenities": "",
                "main_data": "",
                "contact_data": "",
                "original_url": "",
                "post_in_data": datetime.now().strftime("%d.%m.%Y"),
                "post_in_time": datetime.now().strftime("%H:%M"),
                "subcat": "Cits",
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
            result_object["subcat"] = "Dzīvokļi"
        except:
            pass
        try:
            result_object["city"] = infotable["Vieta:"].strip().split(" » ")[-1]
        except:
            pass
        try:
            result_object["street"] = infotable["Iela:"]
        except:
            pass
        try:
            result_object["district"] = infotable["Vieta:"].strip().split(" » ")[-2]
        except:
            pass
        try:
            result_object["area_m2"] = infotable["Platība (m2):"]
        except:
            pass
        try:
            result_object["estate_series"] = infotable["Sērija:"]
        except:
            pass
        try:
            result_object["amenities"] = infotable["Ērtības:"]
        except:
            pass
        try:
            result_object["post_in_data"] = infotable["Pievienots:"].strip().split(" ")[0]
        except:
            pass
        try:
            result_object["post_in_time"] = infotable["Pievienots:"].strip().split(" ")[1]
        except:
            pass

        return result_object
