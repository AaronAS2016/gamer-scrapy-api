import scrapy
import json

from storescraping.utils.url_builder import url_search_build
from storescraping.sites.modes import Validador


class GOGSpider(scrapy.Spider, Validador):
    name = "gog"

    def __init__(self, query, modo, url_search, *args, **kwargs):
        super(GOGSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url_search_build(query, url_search)]
        self.contador = 0
        self.query = query
        self.modo = self.obtener_modo(modo)

    def parse(self, response):
        items = json.loads(response.body)["products"]
        for item in items:
            title = item["title"]
            price = item["price"]["amount"]
            if self.modo(self.query, title.lower()):
                yield {
                    "title" : title,
                    "price" : price,
                    "provider": self.name
                }
