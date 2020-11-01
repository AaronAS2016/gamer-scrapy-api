import scrapy
import json
from storescraping.utils.url_builder import url_builder, get_site_data
from storescraping.sites.parseador import Parseador


class StoreSpider(scrapy.Spider):
    name = "store"

    def __init__(self, query, modo, config, sites_to_search, *args, **kwargs):
        super(StoreSpider, self).__init__(*args, **kwargs)
        self.config = config
        self.start_urls = [url_builder(site, config, query)
                            for site in sites_to_search]
        self.parseador = Parseador()
        self.query = query
        self.modo = modo

    def parse(self, response):
        site_data = get_site_data(response.url, self.config)
        for item in self.parseador.parsear_elements(self.query, response, site_data ):
            yield item
        
