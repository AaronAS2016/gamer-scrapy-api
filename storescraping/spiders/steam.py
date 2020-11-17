import scrapy
import re
import requests
from scrapy import FormRequest, Request
from storescraping.utils.url_builder import url_search_build
from storescraping.sites.spider_site import SpiderSites
from storescraping.config.constant import SIN_PRECIO, URL_API_DOLARES


class SteamSpider(scrapy.Spider, SpiderSites):
    name = "steam"

    selector_items = "//div[@id='search_resultsRows']/a"
    selector_price = ".game_purchase_price::text"
    selector_price_discount = ".discount_final_price::text"
    selector_title = ".//div[@class='apphub_AppName']/text()"
    selector_title_header = ".pageheader::text"
    selector_category = "a.app_tag::text"

    def __init__(self, query, modo, url_search, *args, **kwargs):
        super(SteamSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url_search_build(query, url_search)]
        self.contador = 0
        self.query = query
        self.es_valido_el_resultado = self.obtener_modo_de_busqueda(modo)

    def dolarizar_pesos(self, precio_pesos):
        requester = requests.get(URL_API_DOLARES)
        data = requester.json()
        valor_oficial = float(data[0]['casa']['venta'].replace(",", "."))
        return round(precio_pesos/valor_oficial, 2)

    def parse_product(self, response):
        categories = response.css().get(self.selector_category)
        category = re.sub(r'[\r|\n|\t]', '', str(
            categories[0])) if categories is not None or categories == "" else "Sin Categoria"
        title = response.xpath(self.selector_title).get()
        if title is None:
            title = response.css(self.selector_title_header).get()
        price = str(response.css(self.selector_price).get())
        if price == "None": #Si es None puede ser que es un producto con descuento/ o tipo pack , o que no salio a la venta
            price = str(response.css(self.selector_price_discount).get())
        price = re.sub(r'[\r|\n|\t]', '', price)

        if self.es_valido_el_resultado(self.query, title.lower()) and price != "None": #Si es None significa que es algo que no salio a la venta

            if "Free" in price:
                price = float(0)

            elif "ARS" in price:
                price = float(price.replace("ARS$ ", "").replace(
                    ".", "").replace(",", "."))
                price = self.dolarizar_pesos(price)

            yield {
                "title": title,
                #"price": round(float(str(price).replace("ARS$ ","").replace(".", "").replace(",", "."))*0.013, 2),
                "price": float(price),
                "provider": self.name,
                "category": category,
                "url": response.url
            }

    def parse(self, response):
        items = response.xpath(self.selector_items)

        for item in items:
            link = item.xpath("./@href").get()
            yield response.follow(link, callback=self.parse_product, cookies={'lastagecheckage': '1-0-1931', 'birthtime': "-539125199"})
