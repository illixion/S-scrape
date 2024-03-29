import json
import scrapy
from bs4 import BeautifulSoup
from datetime import datetime
from ..items import EstateItem


class MmEstateSpider(scrapy.Spider):
    name = 'mmlv-estate'
    allowed_domains = ['mm.lv', "im.mm.lv"]
    start_urls = ['https://mm.lv/dzivokli?all', 'https://mm.lv/majas?all']

    def parse(self, response):
        for url in response.xpath('//*[@id="listing-card-list"]/li[contains(@class, "listing-card")]//a/@href').getall():
            yield scrapy.Request(url=url, callback=self.parse_ad)

    def parse_ad(self, response):
        page_html = BeautifulSoup(response.text, "html.parser")
        result = self.parse_mm_estate(page_html, response)

        if result == None:
            return

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
        item["cadastre_number"] = result["cadastre_number"]
        item["amenities"] = result["amenities"],
        item["contact_data"] = result["contact_data"],
        item["original_url"] = response.url,
        item["post_in_data"] = result["post_in_data"],
        item["post_in_time"] = result["post_in_time"],
        item["main_data"] = result["main_data"],
        yield item

    def parse_mm_estate(self, page_html, response):
        images = []
        try:
            for image in page_html.select(".rsTmb"):
                images.append({"title": "Image", "url": image["src"]})
        except:
            pass

        table_elements = response.xpath('//div[@id="custom_fields"]/following-sibling::ul//li//text()').getall()
        try:
            table_elements.remove("Apraksts")
        except ValueError:
            pass

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
            "city": "",
            "district": "",
            "street": "",
            "rooms": "",
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

        try:
            price = page_html.select_one(".currency-value").text
            if "/mēn" in price or "Pērk" in price or "/d" in price:
                return None
            result_object["price"] = "".join(
                i for i in page_html.select_one(".currency-value").text if i.isdigit()
            )
        except:
            pass
        try:
            if infotable[" Darījuma veids"] == "Pērk": return None
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
            result_object["city"] = infotable["Pilsēta"]
        except:
            pass
        try:
            result_object["district"] = infotable["Mikrorajons"]
        except:
            pass
        try:
            result_object["street"] = infotable["Adrese"]
        except:
            pass
        try:
            result_object["rooms"] = infotable[" Istabu skaits"]
        except:
            pass
        try:
            result_object["area_m2"] = infotable[" Platība"]
        except:
            pass
        try:
            result_object["area_m2"] = infotable[" Majas platība"]
        except:
            pass
        try:
            result_object["floor"] = infotable[" Stāvs"]
        except:
            pass
        try:
            result_object["estate_series"] = infotable[" Sērija"]
        except:
            pass
        try:
            result_object["estate_type"] = infotable[" Ēkas tips"]
        except:
            pass
        try:
            result_object["estate_type"] = infotable[" Mājas tips"]
        except:
            pass
        try:
            result_object["amenities"] = infotable[" Ērtības"]
        except:
            pass
        try:
            result_object["subcat"] = (
                page_html.select_one(".breadcrumb").find("li", {"class": "penult"}).text
            )
        except:
            pass

        return result_object
