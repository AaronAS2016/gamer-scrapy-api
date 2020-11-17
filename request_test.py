import requests
import unittest
from storescraping.utils.sort import sort_data
from test_constants import BUSQUEDA_METRO_SIN_ORDENAR, MAYOR_A_MENOR_PRECIO_DE_METRO, MENOR_A_MAYOR_PRECIO_DE_METRO, A_Z_DE_METRO_POR_TITULO, Z_A_DE_METRO_POR_TITULO, METRO_POR_REELEVANCIA
from storescraping.utils.sort import sort_data

BASE_URL = "http://localhost:8080/search"


## TENER LEVANTADA LA API PARA EJECUTAR LOS TESTS 

def buildURL(query, modo="algunas_palabras", orden="default"):
    return f"{BASE_URL}/{modo}/{orden}/{query}"
class RequestTest(unittest.TestCase):
    def test_metroquery(self):
        r = requests.get(buildURL(query="metro"))
        titulo = 'Metro Exodus'
        self.assertEqual(r.json()[0]['title'], titulo)

    def test_sort_metro_by_ascending_price(self):
        r = sort_data(BUSQUEDA_METRO_SIN_ORDENAR, "precio", "asc", "metro")
        self.assertEqual(r, MENOR_A_MAYOR_PRECIO_DE_METRO)

    def test_sort_metro_by_A_Z_name(self):
        r = sort_data(BUSQUEDA_METRO_SIN_ORDENAR, "nombre", "asc", "metro")
        self.assertEqual(r, A_Z_DE_METRO_POR_TITULO)

    def test_sort_metro_by_descending_price(self):
        r = sort_data(BUSQUEDA_METRO_SIN_ORDENAR, "precio", "desc", "metro")
        self.assertEqual(r, MAYOR_A_MENOR_PRECIO_DE_METRO)

    def test_sort_metro_by_Z_A_name(self):
        r = sort_data(BUSQUEDA_METRO_SIN_ORDENAR, "nombre", "desc", "metro")
        self.assertEqual(r, Z_A_DE_METRO_POR_TITULO)

    def test_sort_metro_by_relevance(self):
        r = sort_data(BUSQUEDA_METRO_SIN_ORDENAR,
                      "relevancia", "desc", "metro")
        self.assertEqual(r, METRO_POR_REELEVANCIA)

    def test_busqueda_sin_resultados(self):
        r = requests.get(
            "http://localhost:8080/search/algunas_palabras/precio_asc/minecraft?rango=0&rango=-1")
        rjson = r.json()
        self.assertEqual(rjson, [])


if __name__ == "__main__":
    unittest.main()
