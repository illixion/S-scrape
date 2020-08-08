#!/usr/bin/env python3

import config
import mysql.connector  # Download from http://dev.mysql.com/downloads/connector/python/
import urllib.request
import re
from time import sleep
from bs4 import BeautifulSoup

db = mysql.connector.connect(
    host=config.mysql_host,
    user=config.mysql_user,
    password=config.mysql_pw,
    database=config.mysql_db,
)


def parse_ss(url, lang="lv"):
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

        return {
            "price": ''.join(i for i in page_html.select(".ads_price")[0].span.string if i.isdigit()),
            "model": page_html.find("td", {"id": "tdo_31"}).string,
            "year": page_html.find("td", {"id": "tdo_18"}).string,
            "engine": page_html.find("td", {"id": "tdo_15"}).string,
            "transmission": page_html.find("td", {"id": "tdo_35"}).string,
            "km_travelled": page_html.find("td", {"id": "tdo_16"}).string,
            "color_hex": page_html.find("td", {"id": "tdo_17"}).div["style"][-8:-1],
            "type": page_html.find("td", {"id": "tdo_32"}).string,
            "inspection_until": page_html.find("td", {"id": "tdo_223"}).string,
            "vin": None,  # not implemented
            "plate_no": None,  # not implemented
            "features": parse_car_feature_list(
                page_html.findAll("td", "auto_c_column")
            ),
            "phone": page_html.find("span", {"id": "phone_td_1"}).contents[0].string + ' ' + page_html.find("span", {"id": "phone_td_1"}).contents[1].string,
            "listing_images": listing_images,
        }


def parse_car_feature_list(array_of_td):
    feature_list = []
    for td in array_of_td:
        for feature in td.findAll("img", {"class": "auto_c_img"}):
            if feature.name == "b":
                break
            feature_list.append(feature.find_next("b").text)
    return feature_list


def main():
    cursor = db.cursor()
    cursor.execute(f"select * from {config.source_url_db}")
    sourceURLs = cursor.fetchall()

    for url in sourceURLs:
        result = parse_ss(url[1])

        sql = f"INSERT INTO {config.destination_data_db} (url, price, model, year, engine, transmission, km_travelled, color_hex, type, inspection_until, vin, plate_no, features, phone, listing_images) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (
            url[1],
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

        print(cursor.rowcount, "record inserted.")
        sleep(1)


if __name__ == "__main__":
    main()
