import scrapy
import json
from storescraping.config.config import URL_SCRAPPING
from storescraping.sites.sites import sites
from storescraping.utils.url_builder import url_builder, get_site_data
from storescraping.sites.parseador import Parseador


class StoreSpider(scrapy.Spider):
    name = "store"

    def __init__(self, query, modo, *args, **kwargs):
        super(StoreSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url_builder(url, sites, query)
                            for url in URL_SCRAPPING]
        self.parseador = Parseador()
        self.query = query
        self.modo = modo

    def parse(self, response):
        site_data = get_site_data(response.url, sites)
        yield {
            "items": self.parseador.parsear_elements(self.query, response, site_data )
        }
