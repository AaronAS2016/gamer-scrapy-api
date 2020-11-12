import scrapy
import re
from scrapy import FormRequest, Request
from storescraping.utils.url_builder import url_search_build
from storescraping.sites.modes import Validador
from storescraping.config.constant import SIN_PRECIO


class SteamSpider(scrapy.Spider, Validador):
    name = "steam"

    selector_items = "//div[@id='search_resultsRows']/a"
    selector_price = ".game_purchase_price::text"
    selector_title = ".//div[@class='apphub_AppName']/text()"

    def __init__(self, query, modo, url_search, *args, **kwargs):
        super(SteamSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url_search_build(query, url_search)]
        self.contador = 0
        self.query = query
        self.modo = self.obtener_modo(modo)


    def parse_product(self, response):
        category = re.sub(r'[\r|\n|\t]', '', str(response.css("a.app_tag::text")[0].get()))
        title = response.xpath(self.selector_title).get()
        price = re.sub(r'[\r|\n|\t]', '', str(response.css(self.selector_price).get()))

        if self.modo(self.query, title.lower()):
            yield {
                "title": title,
                "price": price,
                "provider": self.name,
                "link": response.url,
                "category": category
            }

    def parse(self, response):
        items = response.xpath(self.selector_items)

        for item in items:
            link = item.xpath("./@href").get()
            yield response.follow(link, callback=self.parse_product, cookies={'lastagecheckage': '1-0-1931', 'birthtime' : "-539125199"})
