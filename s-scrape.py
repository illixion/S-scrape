#!/usr/bin/env python3

import configparser
import feedparser
import mysql.connector  # Download from http://dev.mysql.com/downloads/connector/python/
import urllib.request
import json
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime

config = configparser.ConfigParser()
config.read("config.ini")
db = mysql.connector.connect(
    host=config["Configuration"]["mysql_host"],
    user=config["Configuration"]["mysql_user"],
    password=config["Configuration"]["mysql_pw"],
    database=config["Configuration"]["mysql_db"],
)


def parse_ss_auto(url):
    page = urllib.request.urlopen(url, timeout=10)
    if page.getcode() == 200:
        page_html = BeautifulSoup(page.read(), "html.parser")

        images = []
        for image in page_html.find_all("img", attrs={"class": "isfoto"}):
            images.append(
                {"title": "Image", "url": image["src"].replace(".t.", ".800.")}
            )

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
                i for i in page_html.select("#tdo_8")[0].string if i.isdigit()
            )
        except:
            pass
        try:
            result_object["thumbnail"] = images[0]["url"]
        except:
            pass
        try:
            result_object["description"] = "\n".join(
                [
                    line.strip()
                    for line in [
                        el.string
                        for el in page_html.find("div", {"id": "msg_div_msg"})
                        if el.string is not None
                    ][1:]
                ]
            )
        except:
            pass
        try:
            result_object["model"] = page_html.find("td", {"id": "tdo_31"}).string
        except:
            pass
        try:
            result_object["year"] = "".join(
                i for i in page_html.find("td", {"id": "tdo_18"}).string if i.isdigit()
            )
        except:
            pass
        try:
            result_object["engine"] = page_html.find("td", {"id": "tdo_15"}).string
        except:
            pass
        try:
            result_object["transmision"] = page_html.find("td", {"id": "tdo_35"}).string
        except:
            pass
        try:
            result_object["mileage"] = "".join(
                i for i in page_html.find("td", {"id": "tdo_16"}).string if i.isdigit()
            )
        except:
            pass
        try:
            result_object["colour"] = page_html.find("td", {"id": "tdo_17"}).text.strip()
        except:
            pass
        try:
            result_object["type"] = page_html.find("td", {"id": "tdo_32"}).string
        except:
            pass
        try:
            result_object["technical_inspection"] = page_html.find("td", {"id": "tdo_223"}).string
        except:
            pass
        try:
            result_object["options_data"] = parse_car_feature_list(page_html.findAll("td", "auto_c_column"))
        except:
            pass
        try:
            result_object["contact_data"] = "".join(
                i for i in page_html.select(".is-7")[0].text[-36:] if i.isdigit()
            )
        except:
            pass
        try:
            result_object["post_in_data"] = page_html.findAll("td", {"class": "msg_footer"})[3].text.split(" ")[1]
        except:
            pass
        try:
            result_object["post_in_time"] = page_html.findAll("td", {"class": "msg_footer"})[3].text.split(" ")[2]
        except:
            pass
        try:
            result_object["images"] = json.dumps(images)
        except:
            pass
        try:
            result_object["subcat"] = page_html.findAll("h2", {"class": "headtitle"})[0].text.split(" / ")[
                1
            ]
        except:
            pass

        return result_object
    else:
        print("connection error:", page.getcode())
        return None

def parse_ss_estate(url):
    page = urllib.request.urlopen(url, timeout=10)
    if page.getcode() == 200:
        page_html = BeautifulSoup(page.read(), "html.parser")

        images = []
        for image in page_html.find_all("img", attrs={"class": "isfoto"}):
            images.append(
                {"title": "Image", "url": image["src"].replace(".t.", ".800.")}
            )

        result_object = {
            "thumbnail": "",
            "description": "",
            "images": "",
            "price": "",
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
        }

        try:
            result_object["price"] = "".join(
                i for i in page_html.select("#tdo_8")[0].string if i.isdigit()
            )
        except:
            pass
        try:
            result_object["thumbnail"] = images[0]["url"]
        except:
            pass
        try:
            result_object["description"] = "\n".join(
                [
                    line.strip()
                    for line in [
                        el.string
                        for el in page_html.find("div", {"id": "msg_div_msg"})
                        if el.string is not None
                    ][1:]
                ]
            )
        except:
            pass
        try:
            result_object["model"] = page_html.find("td", {"id": "tdo_31"}).string
        except:
            pass
        try:
            result_object["year"] = "".join(
                i for i in page_html.find("td", {"id": "tdo_18"}).string if i.isdigit()
            )
        except:
            pass
        try:
            result_object["engine"] = page_html.find("td", {"id": "tdo_15"}).string
        except:
            pass
        try:
            result_object["transmision"] = page_html.find("td", {"id": "tdo_35"}).string
        except:
            pass
        try:
            result_object["mileage"] = "".join(
                i for i in page_html.find("td", {"id": "tdo_16"}).string if i.isdigit()
            )
        except:
            pass
        try:
            result_object["colour"] = page_html.find("td", {"id": "tdo_17"}).text.strip()
        except:
            pass
        try:
            result_object["type"] = page_html.find("td", {"id": "tdo_32"}).string
        except:
            pass
        try:
            result_object["technical_inspection"] = page_html.find("td", {"id": "tdo_223"}).string
        except:
            pass
        try:
            result_object["options_data"] = parse_car_feature_list(page_html.findAll("td", "auto_c_column"))
        except:
            pass
        try:
            result_object["contact_data"] = "".join(
                i for i in page_html.select(".is-7")[0].text[-36:] if i.isdigit()
            )
        except:
            pass
        try:
            result_object["post_in_data"] = page_html.findAll("td", {"class": "msg_footer"})[3].text.split(" ")[1]
        except:
            pass
        try:
            result_object["post_in_time"] = page_html.findAll("td", {"class": "msg_footer"})[3].text.split(" ")[2]
        except:
            pass
        try:
            result_object["images"] = json.dumps(images)
        except:
            pass
        try:
            result_object["subcat"] = page_html.findAll("h2", {"class": "headtitle"})[0].text.split(" / ")[
                1
            ]
        except:
            pass

        return result_object
    else:
        print("connection error:", page.getcode())
        return None


def parse_car_feature_list(array_of_td):
    feature_list = []
    for td in array_of_td:
        for feature in td.findAll("img", {"class": "auto_c_img"}):
            if feature.name == "b":
                break
            thisFeature = feature.find_next("b").text
            feature_list.append({"heading": thisFeature, "item": thisFeature})
    return json.dumps(feature_list)


def parse_autoss(url):
    page = urllib.request.urlopen(url, timeout=10)
    if page.getcode() == 200:
        page_html = BeautifulSoup(page.read(), "html.parser")
        images = []
        for image in page_html.find_all("div", attrs={"class": "is-5"})[0].find_all(
            "img"
        ):
            images.append({"title": "Image", "url": image["src"]})

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
                i for i in page_html.select(".is-7")[0].text[-36:] if i.isdigit()
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
    else:
        print("connection error:", page.getcode())
        return None


def parse_mm_auto(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "text/plain;charset=UTF-8",
        "Origin": "https://mm.lv",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": "https://mm.lv",
        "Cache-Control": "max-age=0",
    }
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req, timeout=10)
    if page.getcode() == 200:
        page_html = BeautifulSoup(page.read(), "html.parser")
        images = []
        for image in page_html.select(".rsTmb"):
            images.append({"title": "Image", "url": image["src"]})

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
            result_object["subcat"] = (
                page_html.select_one(".breadcrumb").find("li", {"class": "penult"}).text
            )
        except:
            pass

        return result_object
    else:
        print("connection error:", page.getcode())
        return None


def parse_reklama_auto(url):
    page = urllib.request.urlopen(url, timeout=10)
    if page.getcode() == 200:
        page_html = BeautifulSoup(page.read(), "html.parser")
        images = []
        for image in page_html.select_one(".coda-nav").findAll("img"):
            images.append({"title": "Image", "url": image["data-src"]})
        infotable = {
            "Marka": "",
            "Gads": "",
            "Dzin.": "",
            "Pārnesumkārba:": "",
            "Nobraukums": "",
            "Krāsa": "",
            "Virsbūve": "",
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
                f"Error while parsing C-data in {url}, reklama might've changed format: {e}"
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
            result_object["subcat"] = infotable["Marka:"]
        except:
            pass

        return result_object
    else:
        print("connection error:", page.getcode())
        return None


def parse_elots_auto(url):
    page = urllib.request.urlopen(url, timeout=10)
    if page.getcode() == 200:
        page_html = BeautifulSoup(page.read(), "html.parser")
        images = []
        for image in page_html.select_one(".bxslider").findAll("img", {"class": "bxslider"}):
            images.append(
                {"title": "Image", "url": image["src"]}
            )

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
                f"Error while parsing C-data in {url}, e-lots might've changed format: {e}"
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
            result_object["subcat"] = infotable["Automašīnas zīmols"].strip()
        except:
            pass

        return result_object
    else:
        print("connection error:", page.getcode())
        return None


def parse_viss_auto(url):
    page = urllib.request.urlopen(url, timeout=10)
    if page.getcode() == 200:
        page_html = BeautifulSoup(page.read(), "html.parser")
        images = []
        for image in page_html.findAll("img", {"class": "maza_bilde"}):
            images.append(
                {"title": "Image", "url": "http://viss.lv" + image["src"]}
            )

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
                f"Error while parsing C-data in {url}, viss might've changed format: {e}"
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
            result_object["subcat"] = infotable["Auto marka:"].strip()
        except:
            pass

        return result_object
    else:
        print("connection error:", page.getcode())
        return None


def main():
    # BEGIN Initial set up
    # ss.com general auto categories
    cursor = db.cursor()
    cursor.execute("select category_name from sub_categories where main_categorie = 1")
    currentCats = [i[0] for i in cursor.fetchall()]

    # ss.com
    catPage = urllib.request.urlopen("https://www.ss.lv/lv/transport/cars/", timeout=10)
    if catPage.getcode() == 200:
        catPage_html = BeautifulSoup(catPage.read(), "html.parser")
        for manufacturer in catPage_html.find("form", {"id": "filter_frm"}).findAll(
            "h4"
        ):
            manufacturer = manufacturer.text
            if manufacturer not in currentCats:
                sql = "INSERT INTO sub_categories (main_categorie, category_filter, category_name, category_description, item_count, url) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (
                    3,
                    None,
                    manufacturer,
                    manufacturer,
                    0,
                    manufacturer.lower().replace(" ", "-"),
                )
                cursor.execute(sql, val)
                db.commit()
    else:
        print("connection to ss.lv failed")

    # autoss.lv
    catPage = urllib.request.urlopen("http://autoss.eu/", timeout=10)
    if catPage.getcode() == 200:
        catPage_html = BeautifulSoup(catPage.read(), "html.parser")
        for manufacturer in catPage_html.select("div.is-multiline")[0].findAll("a"):
            manufacturer = manufacturer.text
            if manufacturer not in currentCats:
                sql = "INSERT INTO sub_categories (main_categorie, category_filter, category_name, category_description, item_count, url) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (
                    3,
                    None,
                    manufacturer,
                    manufacturer,
                    0,
                    manufacturer.lower().replace(" ", "-"),
                )
                cursor.execute(sql, val)
                db.commit()
    else:
        print("connection to autoss.eu failed")

    # zip
    payload = '[["Items__Get",{"_t":48,"pg":1,"url":"/lv/transports/vieglie-auto/?pg=1"},{"Items__Item":["activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemGrouped":["group","group2","place","place2","status","status2","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemGroupedPriced":["currency","group","group2","place","place2","price","status","status2","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemFlat":["address","area","buildingType","coords","currency","features","floor","floors","period","place","place2","price","rooms","series","status","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemCar":["body","brand","color","country","currency","drive","engine","features","fuel","gearbox","gearCount","mileage","model","place","place2","price","ta","vin","year","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemHouse":["address","area","buildingType","coords","currency","features","floors","landArea","period","place","place2","price","rooms","status","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemBike":["brand","currency","engine","model","place","place2","price","year","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemLand":["area","coords","currency","landType","place","place2","price","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemOffice":["address","area","buildingType","coords","currency","floor","floors","place","place2","price","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemBicycle":["brand","currency","model","place","place2","price","year","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemTruck":["brand","currency","engine","model","place","place2","price","vehicleType","year","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemJob":["companyName","companyRegNr","jobType","place","place2","position","workArea","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemTitled":["group","group2","place","place2","status","status2","title","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemTitledPriced":["currency","group","group2","place","place2","price","status","status2","title","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemTitledPlace":["currency","group","group2","place","place2","price","status","status2","title","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemPriced":["currecny","place","place2","price","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemBuyGrouped":["group","group2","place","place2","status","status2","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemFreeStuff":["group","group2","place","place2","status","status2","title","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemGroupedSell":["currency","group","group2","place","place2","price","status","status2","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Categories__Item":["id","parentId","title","icon","isNew","isList","seoUrl","itemCount","meta","parentCategory"]}],["Filters__GetData",{"_t":89,"url":"/lv/transports/vieglie-auto/?pg=1"},{}],["Categories__GetCategory",{"_t":45,"id":69},{"Categories__Item":["id","parentId","title","icon","isNew","isList","seoUrl","itemCount","meta","parentCategory"]}]]'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "text/plain;charset=UTF-8",
        "Origin": "https://zip.lv",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": "https://zip.lv/lv/transports/vieglie-auto/?pg=1",
        "Cache-Control": "max-age=0",
        "TE": "Trailers",
    }
    req = urllib.request.Request(
        "https://zip.lv/api/rpc.php?apikey&uid=0&lang=lv&m=Items__Get%2CFilters__GetData%2CCategories__GetCategory",
        data=payload.encode("ascii"),
        headers=headers,
    )
    page = urllib.request.urlopen(req, timeout=10)
    if page.getcode() == 200:
        json_result = json.loads(page.read())

        for manufacturer in json_result[1][0]["groups"][0]["filters"][0]["values"]:
            manufacturer = manufacturer["caption"]
            if manufacturer not in currentCats:
                sql = "INSERT INTO sub_categories (main_categorie, category_filter, category_name, category_description, item_count, url) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (
                    3,
                    None,
                    manufacturer,
                    manufacturer,
                    0,
                    manufacturer.lower().replace(" ", "-"),
                )
                cursor.execute(sql, val)
                db.commit()

    else:
        print("connection to zip.lv failed")

    # mm.lv
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "text/plain;charset=UTF-8",
        "Origin": "https://mm.lv",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": "https://mm.lv",
        "Cache-Control": "max-age=0",
    }
    req = urllib.request.Request("https://mm.lv/vieglie-auto", headers=headers)
    page = urllib.request.urlopen(req, timeout=10)
    if page.getcode() == 200:
        page_html = BeautifulSoup(page.read(), "html.parser")

        for manufacturer in page_html.select_one(".search-cat-list").findAll(
            "a", href=True
        ):
            manufacturer = manufacturer.text
            if manufacturer not in currentCats:
                sql = "INSERT INTO sub_categories (main_categorie, category_filter, category_name, category_description, item_count, url) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (
                    3,
                    None,
                    manufacturer,
                    manufacturer,
                    0,
                    manufacturer.lower().replace(" ", "-"),
                )
                cursor.execute(sql, val)
                db.commit()

    else:
        print("connection to mm.lv failed")

    # reklama
    catPage = urllib.request.urlopen("https://reklama.bb.lv/lv/transport/cars/menus.html", timeout=10)
    if catPage.getcode() == 200:
        catPage_html = BeautifulSoup(catPage.read(), "html.parser")
        for manufacturer in catPage_html.select_one(".cats").findAll("a", href=True):
            manufacturer = manufacturer.text
            if manufacturer not in currentCats:
                sql = "INSERT INTO sub_categories (main_categorie, category_filter, category_name, category_description, item_count, url) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (
                    3,
                    None,
                    manufacturer,
                    manufacturer,
                    0,
                    manufacturer.lower().replace(" ", "-"),
                )
                cursor.execute(sql, val)
                db.commit()
    else:
        print("connection to reklama failed")

    # e-lots
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "text/plain;charset=UTF-8",
        "Origin": "https://e-lots.lv",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": "https://e-lots.lv",
        "Cache-Control": "max-age=0",
    }
    req = urllib.request.Request("https://e-lots.lv/category/automobili", headers=headers)
    page = urllib.request.urlopen(req, timeout=10)

    if page.getcode() == 200:
        page_html = BeautifulSoup(page.read(), "html.parser")
        for manufacturer in page_html.find("select", {"id": "cf.25"}).findAll("option")[1:]:
            manufacturer = manufacturer.text.strip()
            if manufacturer not in currentCats:
                sql = "INSERT INTO sub_categories (main_categorie, category_filter, category_name, category_description, item_count, url) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (
                    3,
                    None,
                    manufacturer,
                    manufacturer,
                    0,
                    manufacturer.lower().replace(" ", "-"),
                )
                cursor.execute(sql, val)
                db.commit()
    else:
        print("connection to e-lots.lv failed")

    # viss
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "text/plain;charset=UTF-8",
        "Origin": "http://viss.lv",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": "http://viss.lv",
        "Cache-Control": "max-age=0",
    }
    req = urllib.request.Request("http://viss.lv/lv/sludinajumi/c/13/", headers=headers)
    catPage = urllib.request.urlopen(req, timeout=10)

    if catPage.getcode() == 200:
        catPage_html = BeautifulSoup(catPage.read(), "html.parser")
        for manufacturer in catPage_html.select_one(".filtru_tabula").findAll(
            "a", href=True
        ):
            manufacturer = manufacturer.text
            if manufacturer not in currentCats:
                sql = "INSERT INTO sub_categories (main_categorie, category_filter, category_name, category_description, item_count, url) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (
                    3,
                    None,
                    manufacturer,
                    manufacturer,
                    0,
                    manufacturer.lower().replace(" ", "-"),
                )
                cursor.execute(sql, val)
                db.commit()
    else:
        print("connection to autoss.eu failed")

    cursor = db.cursor()
    cursor.execute(
        "select id, category_name from sub_categories where main_categorie = 3"
    )
    currentCats = {}
    for i in cursor.fetchall():
        currentCats[i[1]] = i[0]

    while True:
        # BEGIN main loop

        # ss.lv general auto
        # cursor = db.cursor()
        # cursor.execute(f"select * from {config['Configuration']['source_url_db']}")
        # sourceURLs = cursor.fetchall()

        print("Checking ss.lv feeds")

        # auto
        rss = feedparser.parse("https://www.ss.com/lv/transport/cars/rss/")
        for adEntry in rss["entries"]:
            cursor.execute(
                "SELECT original_url, COUNT(*) FROM category_data WHERE original_url = %s GROUP BY original_url",
                (adEntry["link"],),
            )
            query = cursor.fetchone()
            # gets the number of rows affected by the command executed
            row_count = cursor.rowcount
            if row_count > 0:
                continue

            result = parse_ss_auto(adEntry["link"])

            result['subcat'] = result['subcat'] if result['subcat'] in currentCats else currentCats["Cits"]

            sql = "INSERT INTO category_data (thumbnail, description, images, price, year, engine, transmision, mileage, colour, body_type, technical_inspection, main_data, options_data, original_url, contact_data, post_in_data, post_in_time, sub_categorie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (
                str(result["thumbnail"]),
                str(result["description"]),
                str(result["images"]),
                str(result["price"]),
                str(result["year"]),
                str(result["engine"]),
                str(result["transmision"]),
                str(result["mileage"]),
                str(result["colour"]),
                str(result["type"]),
                str(result["technical_inspection"]),
                str(result["main_data"]),
                str(result["options_data"]),
                str(result["original_url"]),
                str(result["contact_data"]),
                str(result["post_in_data"]),
                str(result["post_in_time"]),
                currentCats[result["subcat"]],
            )
            cursor.execute(sql, val)
            db.commit()

            print(f"Found and saved new entry: {adEntry['link']}")
            sleep(int(config["Configuration"]["pull_delay"]))

        # real estate
        # rss = feedparser.parse("https://www.ss.lv/lv/real-estate/rss/")
        # for adEntry in rss["entries"]:
        #     cursor.execute(
        #         "SELECT original_url, COUNT(*) FROM category_data_estates WHERE original_url = %s GROUP BY original_url",
        #         (adEntry["link"],),
        #     )
        #     query = cursor.fetchone()
        #     # gets the number of rows affected by the command executed
        #     row_count = cursor.rowcount
        #     if row_count > 0:
        #         continue

        #     result = parse_ss_estate(adEntry["link"])

        #     sql = "INSERT INTO category_data_estates (thumbnail, description, images, price, city, district, street, rooms, area_m2, floor, estate_series, estate_type, cadastre_number, amenities, main_data, contact_data, original_url, post_in_data, post_in_time, sub_categorie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        #     val = (
        #         str(result["thumbnail"]),
        #         str(result["description"]),
        #         str(result["images"]),
        #         str(result["price"]),
        #         str(result["year"]),
        #         str(result["engine"]),
        #         str(result["transmision"]),
        #         str(result["mileage"]),
        #         str(result["colour"]),
        #         str(result["type"]),
        #         str(result["technical_inspection"]),
        #         str(result["main_data"]),
        #         str(result["options_data"]),
        #         str(result["original_url"]),
        #         str(result["contact_data"]),
        #         str(result["post_in_data"]),
        #         str(result["post_in_time"]),
        #         6297,
        #     )
        #     cursor.execute(sql, val)
        #     db.commit()

        #     print(f"Found and saved new entry: {adEntry['link']}")
        #     sleep(int(config["Configuration"]["pull_delay"]))

        # autoss
        print("Checking autoss.lv feeds")
        page = urllib.request.urlopen("http://autoss.eu/lv/automasinas?body=&make=&year_from=&year_to=&price_from=&price_to=&mileage_from=&mileage_to=&fuel=&power_from=&power_to=&transmission=&drive_type=&color=&location=&sort=new", timeout=10)
        if page.getcode() == 200:
            page_html = BeautifulSoup(page.read(), "html.parser")
            for elem in page_html.select(".table")[0].find_all("a", {"font-weight": 500})[1:]:
                cursor.execute(
                    "SELECT original_url, COUNT(*) FROM category_data WHERE original_url = %s GROUP BY original_url",
                    (elem["href"],),
                )
                query = cursor.fetchone()  # noqa
                # gets the number of rows affected by the command executed
                row_count = cursor.rowcount
                if row_count > 0:
                    continue

                result = parse_autoss(elem["href"])
                sql = "INSERT INTO category_data (thumbnail, description, images, price, year, engine, transmision, mileage, colour, body_type, technical_inspection, main_data, options_data, original_url, contact_data, post_in_data, post_in_time, sub_categorie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (
                    str(result["thumbnail"]),
                    str(result["description"]),
                    str(result["images"]),
                    str(result["price"]),
                    str(result["year"]),
                    str(result["engine"]),
                    str(result["transmision"]),
                    str(result["mileage"]),
                    str(result["colour"]),
                    str(result["type"]),
                    str(result["technical_inspection"]),
                    str(result["main_data"]),
                    str(result["options_data"]),
                    str(result["original_url"]),
                    str(result["contact_data"]),
                    str(result["post_in_data"]),
                    str(result["post_in_time"]),
                    currentCats[result["subcat"]],
                )
                cursor.execute(sql, val)
                db.commit()

                print("Found and saved new entry:", elem['href'])
                sleep(int(config["Configuration"]["pull_delay"]))

        else:
            print("autoss returned", page.getcode())

        # zip.lv
        print("Checking zip.lv feeds")

        # auto
        payload = '[["Items__Get",{"_t":48,"pg":1,"url":"/lv/transports/vieglie-auto/?pg=1"},{"Items__Item":["activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemGrouped":["group","group2","place","place2","status","status2","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemGroupedPriced":["currency","group","group2","place","place2","price","status","status2","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemFlat":["address","area","buildingType","coords","currency","features","floor","floors","period","place","place2","price","rooms","series","status","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemCar":["body","brand","color","country","currency","drive","engine","features","fuel","gearbox","gearCount","mileage","model","place","place2","price","ta","vin","year","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemHouse":["address","area","buildingType","coords","currency","features","floors","landArea","period","place","place2","price","rooms","status","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemBike":["brand","currency","engine","model","place","place2","price","year","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemLand":["area","coords","currency","landType","place","place2","price","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemOffice":["address","area","buildingType","coords","currency","floor","floors","place","place2","price","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemBicycle":["brand","currency","model","place","place2","price","year","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemTruck":["brand","currency","engine","model","place","place2","price","vehicleType","year","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemJob":["companyName","companyRegNr","jobType","place","place2","position","workArea","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemTitled":["group","group2","place","place2","status","status2","title","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemTitledPriced":["currency","group","group2","place","place2","price","status","status2","title","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemTitledPlace":["currency","group","group2","place","place2","price","status","status2","title","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemPriced":["currecny","place","place2","price","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemBuyGrouped":["group","group2","place","place2","status","status2","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemFreeStuff":["group","group2","place","place2","status","status2","title","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemGroupedSell":["currency","group","group2","place","place2","price","status","status2","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Categories__Item":["id","parentId","title","icon","isNew","isList","seoUrl","itemCount","meta","parentCategory"]}],["Filters__GetData",{"_t":89,"url":"/lv/transports/vieglie-auto/?pg=1"},{}],["Categories__GetCategory",{"_t":45,"id":69},{"Categories__Item":["id","parentId","title","icon","isNew","isList","seoUrl","itemCount","meta","parentCategory"]}]]'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "text/plain;charset=UTF-8",
            "Origin": "https://zip.lv",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://zip.lv/lv/transports/vieglie-auto/?pg=1",
            "Cache-Control": "max-age=0",
            "TE": "Trailers",
        }
        req = urllib.request.Request(
            "https://zip.lv/api/rpc.php?apikey&uid=0&lang=lv&m=Items__Get%2CFilters__GetData%2CCategories__GetCategory",
            data=payload.encode("ascii"),
            headers=headers,
        )
        page = urllib.request.urlopen(req, timeout=10)
        if page.getcode() == 200:
            json_result = json.loads(page.read())

            for result in json_result[0][0]["items"]:
                cursor.execute(
                    "SELECT original_url, COUNT(*) FROM category_data WHERE original_url = %s GROUP BY original_url",
                    (
                        f"https://zip.lv/lv/show/transports/vieglie-auto/?i={result['id']}",
                    ),
                )
                query = cursor.fetchone()  # noqa
                # gets the number of rows affected by the command executed
                row_count = cursor.rowcount
                if row_count > 0:
                    continue

                images = []
                for image in result["images"]:
                    images.append(
                        {"title": "Image", "url": "http:" + image["original"]}
                    )

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
                    result_object["thumbnail"] = images[0]["large"]
                except:
                    pass
                try:
                    result_object["description"] = result["text"]
                except:
                    pass
                try:
                    result_object["images"] = json.dumps(images)
                except:
                    pass
                try:
                    result_object["price"] = result["price"]
                except:
                    pass
                try:
                    result_object["year"] = int(result["year"])
                except:
                    pass
                try:
                    result_object["engine"] = result["fuel"]["caption"]
                except:
                    pass
                try:
                    result_object["transmision"] = result["gearbox"]["caption"]
                except:
                    pass
                try:
                    result_object["mileage"] = result["mileage"]
                except:
                    pass
                try:
                    result_object["colour"] = result["color"]
                except:
                    pass
                try:
                    result_object["type"] = result["body"]["caption"]
                except:
                    pass
                try:
                    result_object["options_data"] = json.dumps([x["caption"] for x in result["features"]])
                except:
                    pass
                try:
                    result_object["original_url"] = f"https://zip.lv/lv/show/transports/vieglie-auto/?i={result['id']}"
                except:
                    pass
                try:
                    result_object["contact_data"] = result["phone"]
                except:
                    pass
                try:
                    result_object["subcat"] = result["brand"]["caption"]
                except:
                    pass
                try:
                    result_object["model"] = result["model"]["caption"]
                except:
                    pass

                sql = "INSERT INTO category_data (thumbnail, description, images, price, year, engine, transmision, mileage, colour, body_type, technical_inspection, main_data, options_data, original_url, contact_data, post_in_data, post_in_time, sub_categorie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (
                    str(result_object["thumbnail"]),
                    str(result_object["description"]),
                    str(result_object["images"]),
                    str(result_object["price"]),
                    str(result_object["year"]),
                    str(result_object["engine"]),
                    str(result_object["transmision"]),
                    str(result_object["mileage"]),
                    str(result_object["colour"]),
                    str(result_object["type"]),
                    str(result_object["technical_inspection"]),
                    str(result_object["main_data"]),
                    str(result_object["options_data"]),
                    str(result_object["original_url"]),
                    str(result_object["contact_data"]),
                    str(result_object["post_in_data"]),
                    str(result_object["post_in_time"]),
                    currentCats[result_object["subcat"]],
                )
                cursor.execute(sql, val)
                db.commit()

                print(
                    f"Found and saved new entry: https://zip.lv/lv/show/transports/vieglie-auto/?i={result['id']}"
                )
                sleep(int(config["Configuration"]["pull_delay"]))
        else:
            print("zip.lv returned", page.getcode())

        # estate
        # payload = '[["Items__Get",{"_t":48,"pg":1,"url":"/ru/nedvizhimost/kvartiri-prodaetsja/?pg=1"},{"Items__Item":["activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemGrouped":["group","group2","place","place2","status","status2","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemGroupedPriced":["currency","group","group2","place","place2","price","status","status2","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemFlat":["address","area","buildingType","coords","currency","features","floor","floors","period","place","place2","price","rooms","series","status","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemCar":["body","brand","color","country","currency","drive","engine","features","fuel","gearbox","gearCount","mileage","model","place","place2","price","ta","vin","year","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemHouse":["address","area","buildingType","coords","currency","features","floors","landArea","period","place","place2","price","rooms","status","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemBike":["brand","currency","engine","model","place","place2","price","year","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemLand":["area","coords","currency","landType","place","place2","price","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemOffice":["address","area","buildingType","coords","currency","floor","floors","place","place2","price","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemBicycle":["brand","currency","model","place","place2","price","year","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemTruck":["brand","currency","engine","model","place","place2","price","vehicleType","year","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemJob":["companyName","companyRegNr","jobType","place","place2","position","workArea","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemTitled":["group","group2","place","place2","status","status2","title","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemTitledPriced":["currency","group","group2","place","place2","price","status","status2","title","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemTitledPlace":["currency","group","group2","place","place2","price","status","status2","title","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemPriced":["currecny","place","place2","price","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemBuyGrouped":["group","group2","place","place2","status","status2","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemFreeStuff":["group","group2","place","place2","status","status2","title","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Items__ItemGroupedSell":["currency","group","group2","place","place2","price","status","status2","activeType","adType","canCall","canOfferPrice","canSendEmail","category","created","email","expires","extUrl","highlighted","id","images","isFavorite","logo","name","phone","phone2","priceOffers","requestedImg","text","type","uid","url","video","views"],"Categories__Item":["id","parentId","title","icon","isNew","isList","seoUrl","itemCount","meta","parentCategory"]}],["Filters__GetData",{"_t":89,"url":"/ru/nedvizhimost/kvartiri-prodaetsja/?pg=1"},{}],["Categories__GetCategory",{"_t":45,"id":63},{"Categories__Item":["id","parentId","title","icon","isNew","isList","seoUrl","itemCount","meta","parentCategory"]}]]'
        # headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0",
        #     "Accept": "*/*",
        #     "Accept-Language": "en-US,en;q=0.5",
        #     "Content-Type": "text/plain;charset=UTF-8",
        #     "Origin": "https://zip.lv",
        #     "DNT": "1",
        #     "Connection": "keep-alive",
        #     "Referer": "https://zip.lv/ru/nedvizhimost/kvartiri-prodaetsja/?pg=1",
        #     "Cache-Control": "max-age=0",
        #     "TE": "Trailers",
        # }
        # req = urllib.request.Request(
        #     "https://zip.lv/api/rpc.php?apikey&uid=0&lang=lv&m=Items__Get%2CFilters__GetData%2CCategories__GetCategory",
        #     data=payload.encode("ascii"),
        #     headers=headers,
        # )
        # page = urllib.request.urlopen(req, timeout=10)
        # if page.getcode() == 200:
        #     json_result = json.loads(page.read())

        #     for result in json_result[0][0]["items"]:
        #         cursor.execute(
        #             "SELECT original_url, COUNT(*) FROM category_data WHERE original_url = %s GROUP BY original_url",
        #             (
        #                 f"https://zip.lv/lv/show/transports/vieglie-auto/?i={result['id']}",
        #             ),
        #         )
        #         query = cursor.fetchone()  # noqa
        #         # gets the number of rows affected by the command executed
        #         row_count = cursor.rowcount
        #         if row_count > 0:
        #             continue

        #         images = []
        #         for image in result["images"]:
        #             images.append(
        #                 {"title": "Image", "url": "http:" + image["original"]}
        #             )

        #         result_object = {
        #             "thumbnail": "",
        #             "description": "",
        #             "images": "",
        #             "price": "0",
        #             "year": "0",
        #             "engine": "",
        #             "transmision": "",
        #             "mileage": "0",
        #             "colour": "",
        #             "type": "",
        #             "technical_inspection": "",
        #             "main_data": "",
        #             "options_data": "",
        #             "original_url": "",
        #             "contact_data": "",
        #             "post_in_data": datetime.now().strftime("%d.%m.%Y"),
        #             "post_in_time": datetime.now().strftime("%H:%M"),
        #             "subcat": "Cits",
        #             "model": "",
        #         }
        #         sql = "INSERT INTO category_data (thumbnail, description, images, price, year, engine, transmision, mileage, colour, body_type, technical_inspection, main_data, options_data, original_url, contact_data, post_in_data, post_in_time, sub_categorie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        #         val = (
        #             str(result["thumbnail"]),
        #             str(result["description"]),
        #             str(result["images"]),
        #             str(result["price"]),
        #             str(result["year"]),
        #             str(result["engine"]),
        #             str(result["transmision"]),
        #             str(result["mileage"]),
        #             str(result["colour"]),
        #             str(result["type"]),
        #             str(result["technical_inspection"]),
        #             str(result["main_data"]),
        #             str(result["options_data"]),
        #             str(result["original_url"]),
        #             str(result["contact_data"]),
        #             str(result["post_in_data"]),
        #             str(result["post_in_time"]),
        #             currentCats[result["subcat"]],
        #         )
        #         cursor.execute(sql, val)
        #         db.commit()

        #         print(
        #             f"Found and saved new entry: https://zip.lv/lv/show/transports/vieglie-auto/?i={result['id']}"
        #         )
        #         sleep(int(config["Configuration"]["pull_delay"]))
        # else:
        #     print("zip.lv returned", page.getcode())

        print("Checking mm.lv feeds")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "text/plain;charset=UTF-8",
            "Origin": "https://mm.lv",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://mm.lv",
            "Cache-Control": "max-age=0",
        }
        req = urllib.request.Request("https://mm.lv/vieglie-auto", headers=headers)
        page = urllib.request.urlopen(req, timeout=10)
        if page.getcode() == 200:
            page_html = BeautifulSoup(page.read(), "html.parser")
            for elem in page_html.select("#listing-card-list")[0].find_all("a"):
                cursor.execute(
                    "SELECT original_url, COUNT(*) FROM category_data WHERE original_url = %s GROUP BY original_url",
                    (elem["href"],),
                )
                query = cursor.fetchone()  # noqa
                # gets the number of rows affected by the command executed
                row_count = cursor.rowcount
                if row_count > 0:
                    continue

                result = parse_mm_auto(elem["href"])
                sql = "INSERT INTO category_data (thumbnail, description, images, price, year, engine, transmision, mileage, colour, body_type, technical_inspection, main_data, options_data, original_url, contact_data, post_in_data, post_in_time, sub_categorie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (
                    str(result["thumbnail"]),
                    str(result["description"]),
                    str(result["images"]),
                    str(result["price"]),
                    str(result["year"]),
                    str(result["engine"]),
                    str(result["transmision"]),
                    str(result["mileage"]),
                    str(result["colour"]),
                    str(result["type"]),
                    str(result["technical_inspection"]),
                    str(result["main_data"]),
                    str(result["options_data"]),
                    str(result["original_url"]),
                    str(result["contact_data"]),
                    str(result["post_in_data"]),
                    str(result["post_in_time"]),
                    currentCats[result["subcat"]],
                )
                cursor.execute(sql, val)
                db.commit()

                print(f"Found and saved new entry: {elem['href']}")
                sleep(int(config["Configuration"]["pull_delay"]))

        else:
            print("mm.lv returned", page.getcode())

        sourceURLs = [
            "https://reklama.bb.lv/lv/transport/cars/sell/table.html?rss",
        ]
        print(f"Checking {len(sourceURLs)} reklama.lv feeds")

        for feedUrl in sourceURLs:
            rss = feedparser.parse(feedUrl)

            for adEntry in rss["entries"]:
                cursor.execute(
                    "SELECT original_url, COUNT(*) FROM category_data WHERE original_url = %s GROUP BY original_url",
                    (adEntry["link"],),
                )
                query = cursor.fetchone()  # noqa
                # gets the number of rows affected by the command executed
                row_count = cursor.rowcount
                if row_count > 0:
                    continue

                result = parse_reklama_auto(adEntry["link"])
                sql = "INSERT INTO category_data (thumbnail, description, images, price, year, engine, transmision, mileage, colour, body_type, technical_inspection, main_data, options_data, original_url, contact_data, post_in_data, post_in_time, sub_categorie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (
                    str(result["thumbnail"]),
                    str(result["description"]),
                    str(result["images"]),
                    str(result["price"]),
                    str(result["year"]),
                    str(result["engine"]),
                    str(result["transmision"]),
                    str(result["mileage"]),
                    str(result["colour"]),
                    str(result["type"]),
                    str(result["technical_inspection"]),
                    str(result["main_data"]),
                    str(result["options_data"]),
                    str(result["original_url"]),
                    str(result["contact_data"]),
                    str(result["post_in_data"]),
                    str(result["post_in_time"]),
                    currentCats[result["subcat"]],
                )
                cursor.execute(sql, val)
                db.commit()

                print(f"Found and saved new entry: {adEntry['link']}")
                sleep(int(config["Configuration"]["pull_delay"]))

        print("Checking e-lots.lv feeds")
        page = urllib.request.urlopen("https://e-lots.lv/category/automobili", timeout=10)

        if page.getcode() == 200:
            page_html = BeautifulSoup(page.read(), "html.parser")
            for elem in page_html.select_one("#postsList").findAll("a", href=True):
                if not elem['href'].endswith(".html"):
                    continue
                cursor.execute(
                    "SELECT original_url, COUNT(*) FROM category_data WHERE original_url = %s GROUP BY original_url",
                    (elem['href'],),
                )
                query = cursor.fetchone()  # noqa
                # gets the number of rows affected by the command executed
                row_count = cursor.rowcount
                if row_count > 0:
                    continue

                result = parse_elots_auto(elem['href'])
                sql = "INSERT INTO category_data (thumbnail, description, images, price, year, engine, transmision, mileage, colour, body_type, technical_inspection, main_data, options_data, original_url, contact_data, post_in_data, post_in_time, sub_categorie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (
                    str(result["thumbnail"]),
                    str(result["description"]),
                    str(result["images"]),
                    str(result["price"]),
                    str(result["year"]),
                    str(result["engine"]),
                    str(result["transmision"]),
                    str(result["mileage"]),
                    str(result["colour"]),
                    str(result["type"]),
                    str(result["technical_inspection"]),
                    str(result["main_data"]),
                    str(result["options_data"]),
                    str(result["original_url"]),
                    str(result["contact_data"]),
                    str(result["post_in_data"]),
                    str(result["post_in_time"]),
                    currentCats[result["subcat"]],
                )
                cursor.execute(sql, val)
                db.commit()

        else:
            print("e-lots.lv returned", page.getcode())

        print("Checking viss.lv feeds")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "text/plain;charset=UTF-8",
            "Origin": "http://viss.lv",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "http://viss.lv",
            "Cache-Control": "max-age=0",
        }
        req = urllib.request.Request("http://viss.lv/lv/sludinajumi/c/13/", headers=headers)
        page = urllib.request.urlopen(req, timeout=10)

        if page.getcode() == 200:
            page_html = BeautifulSoup(page.read(), "html.parser")
            for elem in page_html.select_one(".slud_saraksta_tabula").find_all("a"):
                href = "http://viss.lv" + elem["href"]
                cursor.execute(
                    "SELECT original_url, COUNT(*) FROM category_data WHERE original_url = %s GROUP BY original_url",
                    (href,),
                )
                query = cursor.fetchone()  # noqa
                # gets the number of rows affected by the command executed
                row_count = cursor.rowcount
                if row_count > 0:
                    continue

                result = parse_viss_auto(href)
                sql = "INSERT INTO category_data (thumbnail, description, images, price, year, engine, transmision, mileage, colour, body_type, technical_inspection, main_data, options_data, original_url, contact_data, post_in_data, post_in_time, sub_categorie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (
                    str(result["thumbnail"]),
                    str(result["description"]),
                    str(result["images"]),
                    str(result["price"]),
                    str(result["year"]),
                    str(result["engine"]),
                    str(result["transmision"]),
                    str(result["mileage"]),
                    str(result["colour"]),
                    str(result["type"]),
                    str(result["technical_inspection"]),
                    str(result["main_data"]),
                    str(result["options_data"]),
                    str(result["original_url"]),
                    str(result["contact_data"]),
                    str(result["post_in_data"]),
                    str(result["post_in_time"]),
                    currentCats[result["subcat"]],
                )
                cursor.execute(sql, val)
                db.commit()

        else:
            print("viss returned", page.getcode())

        # BEGIN cooldown
        sleep(int(config["Configuration"]["check_delay"]))


if __name__ == "__main__":
    main()
