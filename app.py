from scrapy.utils.serialize import ScrapyJSONEncoder
import math
import json
from spider_runner import SpiderRunner
from config.config import SITES_TO_SEARCH
from config.sites import CONFIG_SITE
from storescraping.utils.sort import sort_data

from storescraping.spiders.steam import SteamSpider
from storescraping.spiders.gog import GOGSpider
from storescraping.spiders.nuuvem import NuuvemSpider
from storescraping.spiders.gamesplanet import GamesPlantetSpider


from klein import Klein
app = Klein()


@app.route("/")
def index(request):
    return "Good morning sunshine, soon there will be lunch!"


@app.route('/search/<string:modo>/<string:orden>/<string:query>')
async def get_quotes(request, modo, orden, query):
    # CORS
    request.setHeader('Access-Control-Allow-Origin', '*')
    request.setHeader('Access-Control-Allow-Methods', 'GET')
    request.setHeader('Access-Control-Allow-Headers',
                      'x-prototype-version,x-requested-with')
    request.setHeader('Access-Control-Max-Age', "2520")

    runner = SpiderRunner()
    output_data = []
    filtros = None
    rango_minimo, rango_maximo = 0, math.inf
    sitios_a_buscar = SITES_TO_SEARCH

    if b"filtro" in request.args:
        filtros = [filtro.decode("utf-8")
                   for filtro in request.args[b"filtro"]]

    if b"rango" in request.args:
        rango_minimo, rango_maximo = request.args[b"rango"]
        rango_minimo = int(rango_minimo.decode("utf-8"))
        rango_maximo = int(rango_maximo.decode("utf-8"))
        rango_maximo = math.inf if rango_maximo == -1 else rango_maximo

    if filtros is not None:
        sitios_a_buscar = [
            sitio for sitio in sitios_a_buscar if sitio not in filtros]

    _encoder = ScrapyJSONEncoder(ensure_ascii=True)
    for site in sitios_a_buscar:
        if site == "steampowered":
            results = await runner.crawl(SteamSpider, modo=modo, query=query, url_search=CONFIG_SITE[site]["url_search"], rango=(rango_minimo, rango_maximo))
        elif site == "nuuvem":
            results = await runner.crawl(NuuvemSpider, modo=modo, query=query, url_search=CONFIG_SITE[site]["url_search"], rango=(rango_minimo, rango_maximo))
        elif site == "gog":
            results = await runner.crawl(GOGSpider, modo=modo, query=query, url_search=CONFIG_SITE[site]["url_search"], rango=(rango_minimo, rango_maximo))
        elif site == "gamesplanet":
            results = await runner.crawl(GamesPlantetSpider, modo=modo, query=query, url_search=CONFIG_SITE[site]["url_search"], rango=(rango_minimo, rango_maximo))
        output = return_spider_output(results, output_data, site)
        output_data = output
    if orden != "default":
        tipo_orden, indice_orden = orden.split("_")
        output_data = sort_data(output_data, tipo_orden, indice_orden, query)

    return _encoder.encode(output_data)


def return_spider_output(output, output_data, site):
    output_data = output_data + output
    return output_data


app.run("localhost", 8080)
