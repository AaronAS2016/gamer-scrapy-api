import scrapy
from scrapy import Request
import json

from storescraping.utils.url_builder import url_search_build
from storescraping.sites.modes import Validador
from scrapy.http.response.html import HtmlResponse


class NuuvemSpider(scrapy.Spider, Validador):
    name = "nuuvem"

    def __init__(self, query, modo, url_search, *args, **kwargs):
        super(NuuvemSpider, self).__init__(*args, **kwargs)
        self.page = 1
        self.base_url = url_search_build(query, url_search).replace("[PAGE]", str(self.page))
        self.start_urls = [ self.base_url ]
        self.contador = 0
        self.query = query
        self.modo = self.obtener_modo(modo)


    def parse_new_products(self, response:HtmlResponse):
        items = response.css(".product-card--grid")
        print("llega")

        for item in items:
            title = item.css(
                ".product-btn-add-to-cart--container::attr(data-track-product-name)").get()
            price = item.css(
                ".product-btn-add-to-cart--container::attr(data-track-product-price)").get()

            yield {
                "title": title,
                "price": price,
                "provider": self.name
            }

        if response.css(".btn-show-more") is not None:
            self.page += 1
            self.base_url = self.base_url.replace("[PAGE]", str(self.page))
            Request(url=self.base_url, callback=self.parse_new_products)


    def parse(self, response:HtmlResponse):
        if response.css(".btn-show-more") is not None:
            self.page += 1
            self.base_url = self.base_url.replace("[PAGE]", str(self.page))
            return Request(url=self.base_url, callback=self.parse_new_products)