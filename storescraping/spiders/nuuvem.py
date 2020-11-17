import scrapy
from scrapy import Request
import json

from storescraping.utils.url_builder import url_search_build
from storescraping.sites.spider_site import SpiderSites
from storescraping.config.constant import SIN_PRECIO


class NuuvemSpider(scrapy.Spider, SpiderSites):
    name = "nuuvem"
    selector_items = ".product-card--grid"
    selector_price = ".product-price--val::text"
    selector_real_price = ".product-btn-add-to-cart--container::attr(data-track-product-price)"
    selector_title = ".product-title::text"
    selector_category = ".product-btn-add-to-cart--container::attr(data-track-product-genre)"
    selector_link = ".product-card--wrapper::attr(href)"


    def __init__(self, query, modo, url_search, rango, *args, **kwargs):
        super(NuuvemSpider, self).__init__(*args, **kwargs)
        self.page = 1
        self.base_url = url_search_build(query, url_search)
        self.final_url = self.base_url.replace("[PAGE]", str(self.page))
        self.start_urls = [self.final_url]
        self.query = query
        self.rango = rango
        self.es_valido_el_resultado = self.obtener_modo_de_busqueda(modo)

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

            category = item.css(self.selector_category).get()

            link = item.css(self.selector_link).get()

            price = SIN_PRECIO if price == "No disponible" else price_original

            if self.es_valido_el_resultado(self.query, title.lower()) and self.esta_en_rango_de_precio(self.rango, price):
                    yield {
                        "title": title,
                        "price": float(price),
                        "provider": self.name,
                        "category": category,
                        "url": link
                    }

        if len(response.css(".btn-show-more")) > 0:
            self.page += 1
            self.final_url = self.base_url.replace("[PAGE]", str(self.page))
            yield Request(url=self.final_url, callback=self.parse_new_products)
