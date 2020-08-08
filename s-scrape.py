#!/usr/bin/env python3

import config
import mysql.connector
import urllib.request
import re
from bs4 import BeautifulSoup

db = mysql.connector.connect(
    host=config.mysql_db,
    user=config.mysql_user,
    password=config.mysql_pw
)



def parse_ss(url, lang="lv", category="auto"):
    """
    Convert the ss.com/ss.lv link to parsed information.

    Parameters:
    url (string): ss.com/ss.lv URL to parse
    lang (string): lv or ru, specifies language of returned data
    category (string): which category is the ad from (auto/real_estate)

    Returns:
    object: all data that could be extracted from the page, check code for data format

    """

    page = urllib.request.urlopen(url)
    if page.getcode() == 200:
        page_html = BeautifulSoup(page.read(), "html.parser")

        listing_images = []
        for image in page_html.find_all("img", attrs={"class": "isfoto"}):
            listing_images.append(image["src"].replace(".t.", ".800."))

        gps_coordinates = re.match(
            r".*&c=(\d*\.\d*), (\d*\.\d*).*",
            page_html.find("a", {"id": "mnu_map"})["onclick"],
        ).groups()

        if category == "real_estate":
            return {
                "price": page_html.select(".ads_price")[0].string or "",
                "address_street": page_html.find("td", {"id": "tdo_11"}).b.string or "",
                "address_region": page_html.find("td", {"id": "tdo_856"}).b.string or "",
                "address_city": page_html.find("td", {"id": "tdo_20"}).b.string or "",
                "address_gps": [gps_coordinates[0], gps_coordinates[1]],
                "rooms": page_html.find("td", {"id": "tdo_1"}).string or "",
                "sq_meters": page_html.find("td", {"id": "tdo_3"}).string or "",
                "floors": page_html.find("td", {"id": "tdo_4"}).string or "",
                "series": page_html.find("td", {"id": "tdo_6"}).string or "",
                "building_type": page_html.find("td", {"id": "tdo_2"}).string or "",
                "amenities": page_html.find("td", {"id": "tdo_7"}).string or "",
                "phone": page_html.find("td", {"id": "phone_td_1"}).string or "",  # not implemented
                "listing_images": listing_images,
            }

        elif category == "auto":
            return {
                "price": page_html.select(".ads_price")[0].string or "",

                "model": page_html.find("td", {"id": "tdo_31"}).string or "",
                "year": page_html.find("td", {"id": "tdo_18"}).string or "",
                "engine": page_html.find("td", {"id": "tdo_15"}).string or "",
                "transmission": page_html.find("td", {"id": "tdo_35"}).string or "",
                "km_travelled": page_html.find("td", {"id": "tdo_16"}).string or "",
                "color": {
                    "hex": page_html.find("td", {"id": "tdo_17"}).div['style'][-8:-1],
                    "text": page_html.find("td", {"id": "tdo_17"}).text.strip(),
                },
                "type": page_html.find("td", {"id": "tdo_32"}).string or "",
                "inspection_until": page_html.find("td", {"id": "tdo_223"}).string or "",
                "vin": None,  # not implemented
                "plate_no": None,  # not implemented

                "features": parse_car_feature_list(page_html.findAll('td', 'auto_c_column')),

                "phone": page_html.find("td", {"id": "phone_td_1"}).string or "",
                "listing_images": listing_images,
            }

        else:
            raise NotImplementedError(f"{category} is not yet implemented.")


def parse_car_feature_list(array_of_td):
    feature_list = {}
    for td in array_of_td.findAll('td', 'auto_c_column'):
        for feature in td.findAll("img", {"class": "auto_c_img"}):
            if feature.name == "b":
                break
            feature_list.append(feature.find_next("b").text)


# feature_list = {}
# for td in page_html.findAll('td', 'auto_c_column'):
#     nextHeader = td.find("div", {"class": "auto_c_head"})
#     feature_list.setdefault(nextHeader.text, [])
#     # find_all_next
#     for feature in td.findAll("img", {"class": "auto_c_img"}):
#         if feature.name == "b":
#             break
#         feature_list[td.div.text].append(feature.find_next("b").text)

# pprint(feature_list)
