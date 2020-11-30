import json
import scrapy
from bs4 import BeautifulSoup
from datetime import datetime
from ..items import AutoItem


class AutoSsAutoSpider(scrapy.Spider):
    name = 'autoss-auto'
    allowed_domains = ['autoss.eu']
    start_urls = ["http://autoss.eu/lv/automasinas?body=&make=&year_from=&year_to=&price_from=&price_to=&mileage_from=&mileage_to=&fuel=&power_from=&power_to=&transmission=&drive_type=&color=&location=&sort=new"]

    def parse(self, response):
        for url in response.xpath('//table//a[@style="font-weight: 500"]/@href').getall():
            yield scrapy.Request(url=url, callback=self.parse_ad)

    def parse_ad(self, response):
        page_html = BeautifulSoup(response.text, "html.parser")
        result = self.parse_autoss(page_html, response)

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

    def parse_autoss(self, page_html, response):
        images = []
        try:
            for image in page_html.find_all("div", attrs={"class": "is-5"})[0].find_all(
                "img"
            ):
                images.append({"title": "Image", "url": image["src"]})
        except:
            pass

        table = page_html.find("table")
        infotable = {
            "Pirmā reģistrācija": "",
            "Degviela": "",
            "Pārnesumkārba": "",
            "Nobraukums (km)": "",
            "Krāsa": "",
            "Virsbūves tips": "",
        }
        for row in table.findAll("tr"):
            col = row.findAll("td")
            try:
                infotable[col[0].text] = col[1].text
            except IndexError:
                pass

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

        try:
            result_object["price"] = "".join(
                i for i in infotable["Cena"] if i.isdigit()
            )
        except:
            pass
        try:
            result_object["thumbnail"] = images[0]["url"]
        except:
            pass
        try:
            result_object["description"] = page_html.select_one(".is-7").find("p").text
        except:
            pass
        try:
            result_object["model"] = page_html.select(".is-active")[0].text
        except:
            pass
        try:
            result_object["year"] = infotable["Pirmā reģistrācija"].split("/")[-1]
        except:
            pass
        try:
            result_object["engine"] = infotable["Degviela"]
        except:
            pass
        try:
            result_object["transmision"] = infotable["Pārnesumkārba"]
        except:
            pass
        try:
            result_object["mileage"] = "".join(
                i for i in infotable["Nobraukums (km)"] if i.isdigit()
            )
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
            result_object["contact_data"] = "".join(
                i for i in response.xpath('//img[@src="http://autoss.eu/img/phone.svg"]/following-sibling::text()').get().split(";")[0] if i.isdigit()
            )
        except:
            pass
        try:
            result_object["images"] = json.dumps(images)
        except:
            pass
        try:
            result_object["subcat"] = (
                page_html.select(".breadcrumb")[0].ul.findAll("a")[1].text
            )
        except:
            pass

        return result_object
