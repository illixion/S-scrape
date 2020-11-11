#!/usr/bin/env python3

import configparser
import feedparser
import mysql.connector  # Download from http://dev.mysql.com/downloads/connector/python/
import urllib.request
import sys
import json
from time import sleep
from bs4 import BeautifulSoup

config = configparser.ConfigParser()
config.read('config.ini')
db = mysql.connector.connect(
    host=config['Configuration']['mysql_host'],
    user=config['Configuration']['mysql_user'],
    password=config['Configuration']['mysql_pw'],
    database=config['Configuration']['mysql_db'],
)


def parse_ss_auto(url):
    """
    Convert the ss.com/ss.lv car ad link to parsed information.

    Parameters:
    url (string): ss.com/ss.lv URL to parse
    lang (string): lv or ru, specifies language of returned data

    Returns:
    object: all data that could be extracted from the page, check code for data format

    """

    page = urllib.request.urlopen(url)
    if page.getcode() == 200:
        page_html = BeautifulSoup(page.read(), "html.parser")

        listing_images = []
        for image in page_html.find_all("img", attrs={"class": "isfoto"}):
            listing_images.append({"title": "Image", "url": image["src"].replace(".t.", ".800.")})

        try:
            crusty_car_data = [
                {
                    "heading": "Marka",
                    "item": bsFind(page_html, "td", {"id": "tdo_31"}),
                },
                {
                    "heading": "Izlaiduma gads",
                    "item": bsFind(page_html, "td", {"id": "tdo_18"}),
                },
                {
                    "heading": "Motors",
                    "item": bsFind(page_html, "td", {"id": "tdo_15"}),
                },
                {
                    "heading": "Ātr.kārba",
                    "item": bsFind(page_html, "td", {"id": "tdo_35"}),
                },
                {
                    "heading": "Nobraukums, km",
                    "item": bsFind(page_html, "td", {"id": "tdo_16"}),
                },
                {
                    "heading": "Krāsa",
                    "item": bsFind(page_html, "td", {"id": "tdo_17"}, "color"),
                    "color": bsFind(page_html, "td", {"id": "tdo_17"}, "color"),
                },
                {
                    "heading": "Virsūbes tips",
                    "item": bsFind(page_html, "td", {"id": "tdo_32"}),
                },
                {
                    "heading": "Tehniskā skate",
                    "item": bsFind(page_html, "td", {"id": "tdo_223"}),
                }
            ]
        except AttributeError as e:
            print(f"Error while parsing C-data in {url}, ss.com might've changed format: {e}")
            crusty_car_data = []

        try:
            price = ''.join(i for i in bsFind(page_html, "#tdo_8", type="select") if i.isdigit())
        except:
            price = 0
        try:
            main_image = listing_images[0]['url']
        except:
            main_image = ""

        try:
            return {
                "crusty_car_data": json.dumps(crusty_car_data),
                "price": price,
                "description": bsFind(page_html, "", type="description"),
                "model": bsFind(page_html, "td", {"id": "tdo_31"}),
                "year": bsFind(page_html, "td", {"id": "tdo_18"}),
                "engine": bsFind(page_html, "td", {"id": "tdo_15"}),
                "transmission": bsFind(page_html, "td", {"id": "tdo_35"}),
                "km_travelled": bsFind(page_html, "td", {"id": "tdo_16"}),
                "color_hex": bsFind(page_html, "td", {"id": "tdo_17"}, "color"),
                "type": bsFind(page_html, "td", {"id": "tdo_32"}),
                "inspection_until": bsFind(page_html, "td", {"id": "tdo_223"}),
                "vin": None,  # not implemented
                "plate_no": None,  # not implemented
                "features": parse_car_feature_list(
                    page_html.findAll("td", "auto_c_column")
                ),
                "phone": bsFind(page_html, "span", {"id": "phone_td_1"}, "contents", 0) + ' ' + bsFind(page_html, "span", {"id": "phone_td_1"}, "contents", 1),
                "listing_images": json.dumps(listing_images),
                "main_image": main_image,
                "date": bsFind(page_html, "td", {"class": "msg_footer"}, type="date"),
                "time": bsFind(page_html, "td", {"class": "msg_footer"}, type="time"),
                "subcat": bsFind(page_html, "", type="subcat"),
            }
        except AttributeError as e:
            print(f"Error while parsing {url}, ss.com might've changed format: {e}")


def parse_car_feature_list(array_of_td):
    feature_list = []
    for td in array_of_td:
        for feature in td.findAll("img", {"class": "auto_c_img"}):
            if feature.name == "b":
                break
            thisFeature = feature.find_next("b").text
            feature_list.append({"heading": thisFeature, "item": thisFeature})
    return json.dumps(feature_list)


def bsFind(page_html, elem, param={}, type="string", contents_id=0):
    try:
        if type == "string":
            return page_html.find(elem, param).string
        elif type == "div":
            return page_html.find(elem, param).div
        elif type == "contents":
            return page_html.find(elem, param).contents[contents_id].string
        elif type == "select":
            return page_html.select(elem)[0].string
        elif type == "color":
            return page_html.findAll("div", {"class": "ads_color_opt"})[0].attrs['style'][-8:-1]
        elif type == "description":
            return "\n".join([line.strip() for line in [el.string for el in page_html.find("div", {"id": "msg_div_msg"}) if el.string is not None][1:]])
        elif type == "date":
            return page_html.findAll(elem, param)[3].text.split(" ")[1]
        elif type == "time":
            return page_html.findAll(elem, param)[3].text.split(" ")[2]
        elif type == "subcat":
            return page_html.findAll("h2", {"class": "headtitle"})[0].text.split(" / ")[1]
        
    except:
        print(f"couldn't find {elem} with opt {param} in page source")
        return None


def main():
    # Rescan ss.lv categories on launch
    # general auto
    cursor = db.cursor()
    cursor.execute("select category_name from sub_categories where main_categorie = 1")
    currentCats = [i[0] for i in cursor.fetchall()]

    catPage = urllib.request.urlopen("https://www.ss.lv/lv/transport/cars/")
    if catPage.getcode() == 200:
        catPage_html = BeautifulSoup(catPage.read(), "html.parser")
    else:
        sys.exit("Connection to ss.lv/ss.com failed, exiting")

    for manufacturer in catPage_html.find("form", {"id": "filter_frm"}).findAll("h4"):
        manufacturer = manufacturer.text
        if manufacturer not in currentCats:
            sql = "INSERT INTO sub_categories (main_categorie, category_filter, category_name, category_description, item_count, url) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (
                1,
                None,
                manufacturer,
                manufacturer,
                0,
                manufacturer.lower().replace(" ", "-")
            )
            cursor.execute(sql, val)
            db.commit()

    cursor = db.cursor()
    cursor.execute("select id, category_name from sub_categories where main_categorie = 1")
    currentCats = {}
    for i in cursor.fetchall():
        currentCats[i[1]] = i[0]

    while True:
        # cursor = db.cursor()
        # cursor.execute(f"select * from {config['Configuration']['source_url_db']}")
        # sourceURLs = cursor.fetchall()
        sourceURLs = [
            "https://www.ss.com/lv/transport/cars/rss/",
        ]
        print(f"Checking {len(sourceURLs)} feeds")

        for feedUrl in sourceURLs:
            rss = feedparser.parse(feedUrl)

            for adEntry in rss['entries']:
                cursor.execute(
                    "SELECT original_url, COUNT(*) FROM category_data WHERE original_url = %s GROUP BY original_url",
                    (adEntry['link'],)
                )
                query = cursor.fetchone()
                # gets the number of rows affected by the command executed
                row_count = cursor.rowcount
                if row_count > 0:
                    continue

                if True:
                    result = parse_ss_auto(adEntry['link'])
                    sql = f"INSERT INTO category_data (thumbnail, description, images, price, original_url, main_data, options_data, contact_data, post_in_data, post_in_time, sub_categorie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (
                        result['main_image'].replace("https:", ""),
                        result['description'][:254],
                        result['listing_images'],
                        int(result['price']),
                        adEntry['link'],
                        result['crusty_car_data'],
                        result['features'],
                        None,
                        result['date'],
                        result['time'],
                        currentCats[result['subcat']]
                    )
                    cursor.execute(sql, val)
                    db.commit()
                elif True:
                    result = parse_ss_auto(adEntry['link'])
                    sql = f"INSERT INTO {config['Configuration']['destination_data_db']} (url, price, model, year, engine, transmission, km_travelled, color_hex, type, inspection_until, vin, plate_no, features, phone, listing_images) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (
                        adEntry['link'],
                        result['price'],
                        result['model'],
                        result['year'],
                        result['engine'],
                        result['transmission'],
                        result['km_travelled'],
                        result['color_hex'],
                        result['type'],
                        result['inspection_until'],
                        result['vin'],
                        result['plate_no'],
                        ", ".join(result['features']),
                        result['phone'],
                        "|".join(result['listing_images']),
                    )
                    cursor.execute(sql, val)
                    db.commit()

                print(f"Found and saved new entry: {adEntry['link']}")
                sleep(int(config['Configuration']['pull_delay']))
        sleep(int(config['Configuration']['check_delay']))


if __name__ == "__main__":
    main()
