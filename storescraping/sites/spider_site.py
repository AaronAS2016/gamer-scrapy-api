
from storescraping.config.constant import BUSQUEDA_EXACTA, BUSQUEDA_QUE_CONTENGA_ALGUNAS_PALABRAS, BUSQUEDA_QUE_CONTENTA_TODAS_PALABRAS, SIN_PRECIO

class SpiderSites:

    def obtener_modo_de_busqueda(self, modo):
        if modo == BUSQUEDA_EXACTA:
            return self.__modo_escricto
        elif modo == BUSQUEDA_QUE_CONTENGA_ALGUNAS_PALABRAS:
            return self.__modo_algunas_palabras
        elif modo == BUSQUEDA_QUE_CONTENTA_TODAS_PALABRAS:
            return self.__modo_todas_palabras

    #estricto* o exacto*
    def __modo_escricto(self, query, title):
        return query == title

    def __modo_algunas_palabras(self, query, title):
        palabras = query.split(" ")
        return any(palabra in title for palabra in palabras)

    def __modo_todas_palabras(self, query, title):
        palabras = query.split(" ")
        return all(palabra in title for palabra in palabras)


    def esta_en_rango_de_precio(self, rango, precio):
        if precio is None or precio == SIN_PRECIO or precio == "None":
            return False
        rango_minimo, rango_maximo = rango
        return precio <= rango_maximo and precio >= rango_minimo
