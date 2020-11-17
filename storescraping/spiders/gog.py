import scrapy
import json

from storescraping.utils.url_builder import url_search_build
from storescraping.sites.spider_site import SpiderSites
from scrapy import Request


class GOGSpider(scrapy.Spider, SpiderSites):
    name = "gog"

    def __init__(self, query, modo, url_search, rango, *args, **kwargs):
        super(GOGSpider, self).__init__(*args, **kwargs)
        self.page = 1
        self.baseurl = url_search_build(query, url_search)
        self.finalurl = self.baseurl.replace("[PAGE]", str(self.page))
        self.start_urls = [self.finalurl]
        self.query = query
        self.es_valido_el_resultado = self.obtener_modo_de_busqueda(modo)
        self.rango = rango

    def parse(self, response):
        items = json.loads(response.body)["products"]
        if len(items) > 0:
            for item in items:
                title = item["title"]
                price = float(item["price"]["amount"])
                category = item["category"]
                url = item["url"]
                if self.es_valido_el_resultado(self.query, title.lower()) and self.esta_en_rango_de_precio(self.rango, price):
                    yield {
                        "title" : title,
                        "price" : price,
                        "provider": self.name,
                        "category" : category,
                        "url" : "https://www.gog.com" + url,
                    }

            self.page = self.page + 1
            self.finalurl = self.baseurl.replace("[PAGE]", str(self.page))
            yield Request(url=self.finalurl, callback=self.parse)
