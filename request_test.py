import requests, unittest
from storescraping.utils.sort import sort_data
from test_constants import BUSQUEDA_METRO_SIN_ORDENAR, MAYOR_A_MENOR_PRECIO_DE_METRO, MENOR_A_MAYOR_PRECIO_DE_METRO, A_Z_DE_METRO_POR_TITULO, Z_A_DE_METRO_POR_TITULO, A_Z_DE_METRO_POR_PROVEEDOR, Z_A_DE_METRO_POR_PROVEEDOR
from storescraping.utils.sort import sort_data

BASE_URL = "http://localhost:8080/search"

def buildURL(query, modo="algunas_palabras", orden="default"):
    return f"{BASE_URL}/{modo}/{orden}/{query}"
class RequestTest(unittest.TestCase):
    def test_metroquery(self):
        r = requests.get(buildURL(query="metro"))
        titulo = 'Metro Exodus'
        self.assertEqual(r.json()[0]['title'], titulo)

    #data, sort_type, index
    def test_sort_metro_by_ascending_price(self):
        r = sort_data(BUSQUEDA_METRO_SIN_ORDENAR, "precio", "asc")
        self.assertEqual(r, MENOR_A_MAYOR_PRECIO_DE_METRO)

    def test_sort_metro_by_A_Z_name(self):
        r = sort_data(BUSQUEDA_METRO_SIN_ORDENAR, "nombre", "asc")
        self.assertEqual(r, A_Z_DE_METRO_POR_TITULO)

    def test_sort_metro_by_A_Z_provider(self):
        r = sort_data(BUSQUEDA_METRO_SIN_ORDENAR, "pagina", "asc")
        self.assertEqual(r, A_Z_DE_METRO_POR_PROVEEDOR)

    def test_sort_metro_by_descending_price(self):
        r = sort_data(BUSQUEDA_METRO_SIN_ORDENAR, "precio", "desc")
        self.assertEqual(r, MAYOR_A_MENOR_PRECIO_DE_METRO)

    def test_sort_metro_by_Z_A_name(self):
        r = sort_data(BUSQUEDA_METRO_SIN_ORDENAR, "nombre", "desc")
        self.assertEqual(r, Z_A_DE_METRO_POR_TITULO)

    def test_sort_metro_by_Z_A_provider(self):
        r = sort_data(BUSQUEDA_METRO_SIN_ORDENAR, "pagina", "desc")
        self.assertEqual(r, Z_A_DE_METRO_POR_PROVEEDOR)

if __name__ == "__main__":
    unittest.main()
