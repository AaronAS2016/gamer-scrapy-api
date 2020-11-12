from scrapy.utils.serialize import ScrapyJSONEncoder
import json
from spider_runner import SpiderRunner
from config.config import SITES_TO_SEARCH
from config.sites import CONFIG_SITE

from storescraping.spiders.steam import SteamSpider
from storescraping.spiders.gog import GOGSpider
from storescraping.spiders.nuuvem import NuuvemSpider
from storescraping.spiders.gamesplanet import GamesPlantetSpider


from klein import Klein
app = Klein()


@app.route("/")
def index(request):
    return "Good morning sunshine, soon there will be lunch!"


@app.route('/search/<string:modo>/<string:query>')
async def get_quotes(request, modo, query):
    # CORS
    request.setHeader('Access-Control-Allow-Origin', '*')
    request.setHeader('Access-Control-Allow-Methods', 'GET')
    request.setHeader('Access-Control-Allow-Headers', 'x-prototype-version,x-requested-with')
    request.setHeader('Access-Control-Max-Age', "2520")

    runner = SpiderRunner()
    output_data = []


    _encoder = ScrapyJSONEncoder(ensure_ascii=True)
    for site in SITES_TO_SEARCH:
        if site == "steampowered":
            results = await runner.crawl(SteamSpider, modo=modo, query=query, url_search=CONFIG_SITE[site]["url_search"])
        elif site == "nuuvem":
            results = await runner.crawl(NuuvemSpider, modo=modo, query=query, url_search=CONFIG_SITE[site]["url_search"])
        elif site == "gog":
            results = await runner.crawl(GOGSpider, modo=modo, query=query, url_search=CONFIG_SITE[site]["url_search"])
        elif site == "gamesplanet":
            results = await runner.crawl(GamesPlantetSpider, modo=modo, query=query, url_search=CONFIG_SITE[site]["url_search"])
        output = return_spider_output(results, output_data, site )
        output_data = output



    return _encoder.encode(output_data)

def return_spider_output(output, output_data, site):
    output_data = output_data + output
    return output_data


app.run("localhost", 8080)
