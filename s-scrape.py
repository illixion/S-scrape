#!/usr/bin/env python3

import config
import feedparser
import mysql.connector  # Download from http://dev.mysql.com/downloads/connector/python/
import urllib.request
from time import sleep
from bs4 import BeautifulSoup

db = mysql.connector.connect(
    host=config.mysql_host,
    user=config.mysql_user,
    password=config.mysql_pw,
    database=config.mysql_db,
)


def parse_ss(url):
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
            listing_images.append(image["src"].replace(".t.", ".800."))

        try:
            return {
                "price": ''.join(i for i in bsFind(page_html, "#tdo_8", type="select") if i.isdigit()),
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
                "listing_images": listing_images,
            }
        except AttributeError as e:
            print(f"Error while parsing {url}, ss.com might've changed format: {e}")


def parse_car_feature_list(array_of_td):
    feature_list = []
    for td in array_of_td:
        for feature in td.findAll("img", {"class": "auto_c_img"}):
            if feature.name == "b":
                break
            feature_list.append(feature.find_next("b").text)
    return feature_list


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
        elif type == "select":
            return page_html.select(elem, param)["style"][-8:-1]
    except:
        return None


def main():
    while True:
        cursor = db.cursor()
        cursor.execute(f"select * from {config.source_url_db}")
        sourceURLs = cursor.fetchall()
        print(f"Checking {len(sourceURLs)} feeds")

        for feedUrl in sourceURLs:
            rss = feedparser.parse(feedUrl[1])

            for adEntry in rss['entries']:
                cursor.execute(
                    f"SELECT url, COUNT(*) FROM {config.destination_data_db} WHERE url = %s GROUP BY url",
                    (adEntry['link'],)
                )
                query = cursor.fetchone()
                # gets the number of rows affected by the command executed
                row_count = cursor.rowcount
                if row_count > 0:
                    continue

                result = parse_ss(adEntry['link'])

                sql = f"INSERT INTO {config.destination_data_db} (url, price, model, year, engine, transmission, km_travelled, color_hex, type, inspection_until, vin, plate_no, features, phone, listing_images) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
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
                sleep(1)
        sleep(config.delay)


if __name__ == "__main__":
    main()
