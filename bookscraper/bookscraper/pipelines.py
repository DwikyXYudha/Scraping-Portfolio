# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != "product_description":
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()

        # Category & Product Type ---> Swich to lowercase
        lowercase_keys = ["product_type", "category"]
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        # Price ---> convert to float
        price_keys = ["price_excl_tax", "price_incl_tax", "tax"]
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace("£", "")
            adapter[price_key] = float(value)

        # Availability ---> extract number of book in stock
        availability_string = adapter.get("availability")
        adapter["availability"] = int(re.search(r"\d+", availability_string).group())

        # Review ---> convert string to number
        num_reviews_string = adapter.get("num_reviews")
        adapter["num_reviews"] = int(num_reviews_string)

        # Rating ---> convert text to number
        stars_rating = adapter.get("rating")
        split_stars_array = stars_rating.split(" ")
        stars_text_value = split_stars_array[1].lower()
        if stars_text_value == "zero":
            adapter["rating"] = 0
        elif stars_text_value == "one":
            adapter["rating"] = 1
        elif stars_text_value == "two":
            adapter["rating"] = 2
        elif stars_text_value == "three":
            adapter["rating"] = 3
        elif stars_text_value == "four":
            adapter["rating"] = 4
        elif stars_text_value == "five":
            adapter["rating"] = 5

        return item
