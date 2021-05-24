import json
import scrapy
from bs4 import BeautifulSoup
from datetime import datetime
from ..items import EstateItem


class ReklamaEstateSpider(scrapy.Spider):
    name = 'reklama-estate'
    allowed_domains = ['reklama.bb.lv']
    start_urls = ["https://reklama.bb.lv/lv/realty/apartments/sell/table.html?rss"]

    def parse(self, response):
        for url in response.xpath("//channel/item/link/text()").getall():
            yield scrapy.Request(url=url, callback=self.parse_ad)

    def parse_ad(self, response):
        page_html = BeautifulSoup(response.text, "html.parser")
        result = self.parse_reklama_estate(page_html)

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

    def parse_reklama_estate(self, page_html):
        images = []
        try:
            for image in page_html.select_one(".coda-nav").findAll("img"):
                images.append({"title": "Image", "url": image["data-src"]})
        except:
            pass

        infotable = {
            "Operācija": "",
            "Novietojums": "",
            "Istabu skaits": "",
            "Projekts": "",
            "Vieta": "",
            "Stāvs": "",
            "skaits": "",
            "Plat., kv. m": "",
            "Ērtības": "",
            "Vieta": "",
            "Mājas tips": "",
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
                f"Error while parsing C-data in , reklama might've changed format: {e}"
            )
            return None

        try:
            result_object["price"] = "".join(
                i for i in page_html.select_one("#price-full").text if i.isdigit()
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
            result_object["city"] = infotable["Novietojums"].split(", ")[0]
        except:
            pass
        try:
            result_object["district"] = infotable["Novietojums"].split(", ")[1]
        except:
            pass
        try:
            result_object["street"] = infotable["Vieta"]
        except:
            pass
        try:
            result_object["rooms"] = infotable["Istabu skaits"]
        except:
            pass
        try:
            result_object["area_m2"] = infotable["Plat., kv.\xa0m"]
        except:
            pass
        try:
            result_object["floor"] = infotable["Stāvs"]
        except:
            pass
        try:
            result_object["estate_series"] = infotable["Projekts"]
        except:
            pass
        try:
            result_object["estate_type"] = infotable["Mājas tips"]
        except:
            pass
        try:
            result_object["amenities"] = infotable["Ērtības"]
        except:
            pass
        try:
            result_object["subcat"] = infotable["Operācija"]
        except:
            pass

        return result_object
