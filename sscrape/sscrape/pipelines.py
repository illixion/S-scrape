# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector
import json


class SscrapePipeline:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="127.0.0.1",
            user="sscrape",
            password="***REMOVED***",
            database="***REMOVED***",
        )
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        if "category" in item:
            self.cursor.execute(
                "SELECT category_name, COUNT(*) FROM sub_categories WHERE category_name = %s GROUP BY category_name",
                (item["category"],),
            )
            query = self.cursor.fetchone()
            # gets the number of rows affected by the command executed
            row_count = self.cursor.rowcount
            if row_count > 0:
                return item

            sql = "INSERT INTO sub_categories (main_categorie, category_filter, category_name, category_description, item_count, url) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (
                3,
                None,
                item["category"],
                item["category"],
                0,
                item["category"].lower().replace(" ", "-"),
            )
            self.cursor.execute(sql, val)
            self.db.commit()
        elif "city" in item:
            self.cursor.execute(
                "SELECT original_url, COUNT(*) FROM category_data WHERE original_url = %s GROUP BY original_url",
                (''.join(item["original_url"]),),
            )
            query = self.cursor.fetchone()
            # gets the number of rows affected by the command executed
            row_count = self.cursor.rowcount
            if row_count > 0:
                return item
            self.cursor.execute(
                "select id, category_name from sub_categories where main_categorie = 4"
            )
            currentCats = {}
            for i in self.cursor.fetchall():
                currentCats[i[1]] = i[0]

            sql = "INSERT INTO category_data_estates (thumbnail, description, images, price, city, district, street, rooms, area_m2, floor, estate_series, estate_type, cadastre_number, amenities, main_data, contact_data, original_url, post_in_data, post_in_time, sub_categorie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (
                str(''.join(item["thumbnail"])),
                str('\n'.join(item["description"]))[:5000],
                str(''.join(item["images"])),
                str(''.join(item["price"])),
                str(''.join(item["city"])),
                str(''.join(item["district"])),
                str(''.join(item["street"])),
                str(''.join(item["rooms"])),
                str(''.join(item["area_m2"])),
                str(''.join(item["floor"])),
                str(''.join(item["estate_series"])),
                str(''.join(item["estate_type"])),
                str(''.join(item["cadastre_number"])),
                str(''.join(item["amenities"])),
                json.dumps(item.__dict__),
                str(''.join(item["contact_data"])),
                str(''.join(item["original_url"])),
                str(''.join(item["post_in_data"])),
                str(''.join(item["post_in_time"])),
                7587,
            )
            self.cursor.execute(sql, val)
            self.db.commit()
        else:
            self.cursor.execute(
                "SELECT original_url, COUNT(*) FROM category_data WHERE original_url = %s GROUP BY original_url",
                (''.join(item["original_url"]),),
            )
            query = self.cursor.fetchone()
            # gets the number of rows affected by the command executed
            row_count = self.cursor.rowcount
            if row_count > 0:
                return item
            self.cursor.execute(
                "select id, category_name from sub_categories where main_categorie = 3"
            )
            currentCats = {}
            for i in self.cursor.fetchall():
                currentCats[i[1]] = i[0]

            sql = "INSERT INTO category_data (thumbnail, description, images, price, year, engine, transmision, mileage, colour, body_type, technical_inspection, main_data, options_data, original_url, contact_data, post_in_data, post_in_time, sub_categorie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (
                str(''.join(item["thumbnail"])),
                str('\n'.join(item["description"]))[:5000],
                str(''.join(item["images"])),
                str(''.join(item["price"])),
                str(''.join(item["year"])),
                str(''.join(item["engine"])),
                str(''.join(item["transmision"])),
                str(''.join(item["mileage"])),
                str(''.join(item["colour"])),
                str(''.join(item["type"])),
                str(''.join(item["technical_inspection"])),
                json.dumps(item.__dict__),
                str(''.join(item["options_data"])),
                str(''.join(item["original_url"])),
                str(''.join(item["contact_data"])),
                str(''.join(item["post_in_data"])),
                str(''.join(item["post_in_time"])),
                currentCats[''.join(item["subcat"])],
            )
            self.cursor.execute(sql, val)
            self.db.commit()

        return item
