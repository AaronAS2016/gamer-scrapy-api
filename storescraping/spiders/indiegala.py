import scrapy

from storescraping.utils.url_builder import url_search_build
from storescraping.sites.modes import Validador


class IndieGalaSpider(scrapy.Spider, Validador):
    name = "indie"

    def __init__(self, query, modo, url_search, *args, **kwargs):
        super(IndieGalaSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url_search_build(query, url_search)]
        self.contador = 0
        self.query = query
        self.modo = self.obtener_modo(modo)

    def parse(self, response):
        
        yield {
            "title" : "Completar spider"
        }
