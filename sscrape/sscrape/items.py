# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SscrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AutoItem(scrapy.Item):
    thumbnail = scrapy.Field()
    description = scrapy.Field()
    images = scrapy.Field()
    price = scrapy.Field()
    year = scrapy.Field()
    engine = scrapy.Field()
    transmision = scrapy.Field()
    mileage = scrapy.Field()
    colour = scrapy.Field()
    type = scrapy.Field()
    technical_inspection = scrapy.Field()
    main_data = scrapy.Field()
    options_data = scrapy.Field()
    original_url = scrapy.Field()
    contact_data = scrapy.Field()
    post_in_data = scrapy.Field()
    post_in_time = scrapy.Field()
    subcat = scrapy.Field()
    model = scrapy.Field()


class EstateItem(scrapy.Item):
    thumbnail = scrapy.Field()
    description = scrapy.Field()
    images = scrapy.Field()
    price = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    street = scrapy.Field()
    rooms = scrapy.Field()
    area_m2 = scrapy.Field()
    floor = scrapy.Field()
    estate_series = scrapy.Field()
    estate_type = scrapy.Field()
    cadastre_number = scrapy.Field()
    amenities = scrapy.Field()
    main_data = scrapy.Field()
    contact_data = scrapy.Field()
    original_url = scrapy.Field()
    post_in_data = scrapy.Field()
    post_in_time = scrapy.Field()
