import scrapy
import json

from storescraping.utils.url_builder import url_search_build
from storescraping.sites.modes import Validador
from scrapy import Request


class GOGSpider(scrapy.Spider, Validador):
    name = "gog"

    def __init__(self, query, modo, url_search, *args, **kwargs):
        super(GOGSpider, self).__init__(*args, **kwargs)
        self.page = 1
        self.baseurl = url_search_build(query, url_search)
        self.finalurl = self.baseurl.replace("[PAGE]", str(self.page))
        self.start_urls = [self.finalurl]
        self.contador = 0
        self.query = query
        self.modo = self.obtener_modo(modo)

    def parse(self, response):
        items = json.loads(response.body)["products"]
        if len(items) > 0:
            for item in items:
                title = item["title"]
                price = item["price"]["amount"]
                if self.modo(self.query, title.lower()):
                    yield {
                        "title" : title,
                        "price" : price,
                        "provider": self.name,
                        "page": self.page
                    }

            self.page = self.page + 1
            self.finalurl = self.baseurl.replace("[PAGE]", str(self.page))
            yield Request(url=self.finalurl, callback=self.parse)
