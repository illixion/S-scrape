import json
import scrapy
from bs4 import BeautifulSoup
from datetime import datetime
from ..items import EstateItem


class ELotsEstateSpider(scrapy.Spider):
    name = 'elots-estate'
    allowed_domains = ['e-lots.lv']
    start_urls = ["https://e-lots.lv/category/nekustamais-ipasums"]

    def parse(self, response):
        for url in response.xpath('//*[@id="postsList"]//a[not(contains(@href,"search"))]/@href').getall():
            yield scrapy.Request(url=url, callback=self.parse_ad)

    def parse_ad(self, response):
        page_html = BeautifulSoup(response.text, "html.parser")
        result = self.parse_elots_estate(page_html, response)

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

    def parse_elots_estate(self, page_html, response={}):
        images = []
        try:
            for image in page_html.select_one(".bxslider").findAll("img", {"class": "bxslider"}):
                images.append(
                    {"title": "Image", "url": image["src"]}
                )
        except:
            pass

        infotable = {
            "Mājā stāvu": "",
            "Istabas": "",
            "Stāvs": "",
            "Platība": "",
            "Mēbelēts": "",
            "Celtnes tips": "",
            "Zemes platība": "",
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
            result_object["subcat"] = infotable["Celtnes tips"].strip()
        except:
            pass
        try:
            result_object["thumbnail"] = images[0]["url"]
        except:
            pass
        try:
            result_object["rooms"] = infotable["Istabas"].strip()
        except:
            pass
        try:
            result_object["area_m2"] = infotable["Platība"].strip()
        except:
            pass
        try:
            result_object["floor"] = infotable["Stāvs"].strip()
        except:
            pass
        try:
            result_object["city"] = response.xpath("/html/body/div[1]/div[4]/div[2]/div/div[2]/aside/div[1]/div[2]/div[1]/div[1]/div[2]/span/a/text()").get().strip()
        except:
            pass
        try:
            result_object["amenities"] = infotable["Mēbelēts"].strip()
        except:
            pass

        return result_object
