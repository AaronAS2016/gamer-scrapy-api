import scrapy

from storescraping.utils.url_builder import url_search_build
from storescraping.sites.modes import Validador


class EpicSpider(scrapy.Spider, Validador):
    name = "epic"

    def __init__(self, query, modo, url_search, *args, **kwargs):
        super(EpicSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url_search_build(query, url_search)]
        self.contador = 0
        self.query = query
        self.modo = self.obtener_modo(modo)

    def parse(self, response):

        yield {
            "title" : "Completar spider"
        }
