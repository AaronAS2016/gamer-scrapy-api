import scrapy
from scrapy import Request
import json

from storescraping.utils.url_builder import url_search_build
from storescraping.sites.modes import Validador
from storescraping.config.constant import SIN_PRECIO


class NuuvemSpider(scrapy.Spider, Validador):
    name = "nuuvem"
    selector_items = ".product-card--grid"
    selector_price = ".product-price--val::text"
    selector_real_price = ".product-btn-add-to-cart--container::attr(data-track-product-price)"
    selector_title = ".product-title::text"

    def __init__(self, query, modo, url_search, *args, **kwargs):
        super(NuuvemSpider, self).__init__(*args, **kwargs)
        self.page = 1
        self.base_url = url_search_build(query, url_search)
        self.final_url = self.base_url.replace("[PAGE]", str(self.page))
        self.start_urls = [self.final_url]
        self.contador = 0
        self.query = query
        self.modo = self.obtener_modo(modo)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse_new_products)

    def parse_new_products(self, response):
        items = response.css(self.selector_items)

        for item in items:
            title = item.css(
                self.selector_title).get()

            price_original = item.css(
                self.selector_real_price).get().strip()
            price = item.css(
                self.selector_price).get().strip()

            if self.modo(self.query, title.lower()):
                price = SIN_PRECIO if price == "No disponible" else price_original
                yield {
                    "title": title,
                    "price": price,
                    "provider": self.name
                }

        if len(response.css(".btn-show-more")) > 0:
            self.page += 1
            self.final_url = self.base_url.replace("[PAGE]", str(self.page))
            yield Request(url=self.final_url, callback=self.parse_new_products)
