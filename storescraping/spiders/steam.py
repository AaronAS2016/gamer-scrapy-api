import scrapy

from storescraping.utils.url_builder import url_search_build
from storescraping.sites.modes import Validador
from storescraping.config.constant import SIN_PRECIO


class SteamSpider(scrapy.Spider, Validador):
    name = "steam"

    selector_items = "//div[@id='search_resultsRows']/a"
    selector_price = ".search_price::text"
    selector_title = ".//span[@class='title']/text()"

    def __init__(self, query, modo, url_search, *args, **kwargs):
        super(SteamSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url_search_build(query, url_search)]
        self.contador = 0
        self.query = query
        self.modo = self.obtener_modo(modo)

    def parse(self, response):
        items = response.xpath(self.selector_items)

        for item in items:
            title: str = item.xpath(self.selector_title).get()
            price: int = item.css(self.selector_price).get().strip()

            if self.modo(self.query, title.lower()):
                self.contador += 1
                if not price:
                    try:
                        price = item.css(self.selector_price).getall()[
                            1].strip()
                    except IndexError:
                        price = SIN_PRECIO
                yield {
                    "title": title,
                    "price": price,
                    "provider": self.name
                }
