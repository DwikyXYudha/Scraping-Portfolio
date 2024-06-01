import scrapy

from bookscraper.items import BookItem


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    # custom_settings = {
    #     "FEEDS": {
    #         "bookscrape.json" : {"format": "json", "overwrite": True}
    #          }
    # }

    def parse(self, response):
        books = response.css("article.product_pod")

        for book in books:
            relative_url = book.css("h3 a ::attr(href)").get()
            yield response.follow(relative_url, callback=self.parse_book_page)

        next_page = response.css("li.next a ::attr(href)").get()

        if next_page is not None:
            if "catalogue/" in next_page:
                next_page_url = "http://books.toscrape.com/" + next_page
            else:
                next_page_url = "http://books.toscrape.com/catalogue/" + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_page(self, response):
        table_rows = response.css("table tr")
        book_item = BookItem()
        book_item["name"] = response.css("div h1::text").get()
        book_item["image"] = (
            "http://books.toscrape.com/"
            + response.css("div.item img ::attr(src)").get()[5:]
        )
        book_item["url"] = response.url
        book_item["rating"] = response.css("p.star-rating").attrib["class"]
        book_item["upc"] = table_rows[0].css("td ::text").get()
        book_item["product_type"] = table_rows[1].css("td ::text").get()
        book_item["price_excl_tax"] = table_rows[2].css("td ::text").get()
        book_item["price_incl_tax"] = table_rows[3].css("td ::text").get()
        book_item["tax"] = table_rows[4].css("td ::text").get()
        book_item["availability"] = table_rows[5].css("td ::text").get()
        book_item["num_reviews"] = table_rows[6].css("td ::text").get()
        book_item["category"] = response.css("ul.breadcrumb li a::text")[2].get()
        book_item["product_description"] = response.xpath(
            '//*[@id="content_inner"]/article/p/text()'
        ).get()
        yield book_item
