import scrapy

from storescraping.utils.url_builder import url_search_build
from storescraping.sites.spider_site import SpiderSites


class GamesPlantetSpider(scrapy.Spider, SpiderSites):
    name = "gamesplanet"

    selector_items = "//div[@class='row no-gutters game_list game_list_small pt-2']"
    selector_price = ".//span[@class='price_current']/text()"
    selector_title = ".//a[@class='d-block text-decoration-none stretched-link']/text()"
    selector_forward = ".next-page::attr(href)"
    selector_href = ".d-block.text-decoration-none.stretched-link::attr(href)"
    selector_category = ".//span[@class='d-none d-sm-inline-block']/a/text()"

    def __init__(self, query, modo, url_search, rango, *args, **kwargs):
        super(GamesPlantetSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url_search_build(query, url_search)]
        self.contador = 0
        self.query = query
        self.es_valido_el_resultado = self.obtener_modo_de_busqueda(modo)
        self.rango = rango

    def parse(self, response):
        if self.selector_forward is not None:
            items = response.xpath(self.selector_items)
            for item in items:
                title: str = item.xpath(self.selector_title).get()
                original_price: float = item.xpath(self.selector_price).get()
                href: str = "https://us.gamesplanet.com" + \
                    item.css(self.selector_href).get()
                category: str = item.xpath(self.selector_category).get()
                if category is None:
                    category = "Presale"

                if original_price is not None:
                    price = float(original_price.replace("$", ""))

                if self.es_valido_el_resultado(self.query, title.lower()) and self.esta_en_rango_de_precio(self.rango, price):
                    yield {
                        "title": title,
                        "price": price,
                        "provider": self.name,
                        "category": category,
                        "url": href
                    }
            if response.css(self.selector_forward).get():
                yield response.follow(response.css(self.selector_forward).get(), callback=self.parse)
