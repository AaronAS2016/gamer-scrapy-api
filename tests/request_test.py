import requests, unittest


BASE_URL = "http://localhost:8080/search"


def buildURL(query, modo="algunas_palabras"):
    return f"{BASE_URL}/{modo}/{query}"
class RequestTest(unittest.TestCase):
    def test_metroquery(self):
        r = requests.get(buildURL(query="metro"))
        titulo = 'Metro Exodus'
        self.assertEqual(r.json()[0]['title'], titulo)


if __name__ == "__main__":
    unittest.main()