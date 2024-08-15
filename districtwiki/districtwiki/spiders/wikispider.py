import re

import scrapy

from districtwiki.items import DistrictwikiItem


class WikispiderSpider(scrapy.Spider):
    name = "wikispider"
    allowed_domains = ["id.wikipedia.org"]
    start_urls = [
        "https://id.wikipedia.org/wiki/Daftar_kecamatan_dan_kelurahan_di_Indonesia"
    ]

    def parse(self, response):
        table = response.css("table.wikitable")[0]
        base_link = "https://id.wikipedia.org/"
        for row in table.css("tr"):
            cell = row.css("td")
            if cell:
                province = cell.css("::text").get()
                if province:
                    province = re.sub(r"\s+", " ", province).strip()
                    if province == "7150":
                        break
                    item = DistrictwikiItem()
                    item["province"] = province
                    item["city"] = None
                    item["districts"] = []

                relative_link = cell.css("::attr(href)").get()
                if relative_link and "cite_note-6" not in relative_link:
                    province_link = base_link + relative_link
                    yield response.follow(
                        province_link, callback=self.parse_city, meta={"item": item}
                    )
                else:
                    yield item

    def parse_city(self, response):
        item = response.meta["item"]
        province = item["province"]

        base_link = "https://id.wikipedia.org/"
        table = response.css("table.wikitable")[0]
        for row in table.css("tr"):
            cell = row.css("td")
            city = cell.css("a::text").get()
            if city:
                city = re.sub(r"\s+", " ", city).strip()
                city_item = DistrictwikiItem(province=province, city=city, districts=[])
            relative_link = cell.css("::attr(href)").get()
            if relative_link is not None:
                city_link = base_link + relative_link
                yield response.follow(
                    city_link, callback=self.parse_district, meta={"item": city_item}
                )

    def parse_district(self, response):
        item = response.meta["item"]
        table = response.css("table.wikitable")[0]
        for row in table.css("tr"):
            cell = row.css("td")
            district = cell.css("a::text").get()
            if district:
                district = re.sub(r"\s+", " ", district).strip()
                item["districts"].append(district)
        yield item
