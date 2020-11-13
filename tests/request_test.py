import requests, unittest

class RequestTest(unittest.TestCase):
    def test_metroquery(self):
        r = requests.get('http://localhost:8080/search/algunas_palabras/metro')
        titulo = 'Metro Exodus'
        assert (r.json()[0]['title'] == titulo)