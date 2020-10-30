import scrapy
import storescraping.config.constant as constans



class Parseador:

    def parsear_elements(self, query, response, site_data):
        tipo_de_pagina = site_data["type"]
        informacion_recolectada = []
        if tipo_de_pagina == constans.CON_PAGINACION:
            informacion_recolectada = self.__parsear_elements_pagination(
                query, response, site_data)
        elif tipo_de_pagina == constans.CON_INFINITE_SCROLL:
            informacion_recolectada = self.__parsear_elements_infinite_scroll(
                query, response, site_data)
        return informacion_recolectada

    def __parsear_elements_pagination(self, query, response, site_data):
        return 0

    #TODO: solo trae la primera tanda, no sigue analizando si hay mas valores
    def __parsear_elements_infinite_scroll(self, query, response, site_data):
        selector_elements = site_data["parse_elements"]
        selector_items = selector_elements["items"]

        selector_title = selector_elements["title"]
        selector_price = selector_elements["price"]
        selector_img = selector_elements["img_url"]

        informacion_recolectada = []

        items = self.__obtener_elemento(selector_items, response)

        for item in items:
            informacion_recolectada.append({
                "title": self.__obtener_elemento(selector_title, item).get(),
                "price": self.__obtener_elemento(selector_price, item).get().strip(),
                "img": self.__obtener_elemento(selector_img, item).get()
            })

        return informacion_recolectada

    def __obtener_elemento(self, selector, response):
        tipo_de_selector = selector["type"]
        data = None
        if tipo_de_selector == "css":
            data = response.css(selector["selector"])
        else:
            data = response.xpath(selector["selector"])
        return data
