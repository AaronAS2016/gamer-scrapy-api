from scrapy.utils.serialize import ScrapyJSONEncoder
import json
from spider_runner import SpiderRunner
from config.config import SITES_TO_SEARCH
from config.sites import CONFIG_SITE

from storescraping.spiders.steam import SteamSpider
from storescraping.spiders.store import StoreSpider
from storescraping.spiders.test import TestSpider


from klein import Klein
app = Klein()


@app.route("/")
def index(request):
    return "Good morning sunshine, soon there will be lunch!"


@app.route('/search/<string:modo>/<string:query>')
def get_quotes(request, modo, query):
    request.setHeader('Access-Control-Allow-Origin', '*')
    request.setHeader('Access-Control-Allow-Methods', 'GET')
    request.setHeader('Access-Control-Allow-Headers', 'x-prototype-version,x-requested-with')
    request.setHeader('Access-Control-Max-Age', "2520")
    
    runner = SpiderRunner()

    deferred = runner.crawl(SteamSpider, modo=modo, query=query, url_search=CONFIG_SITE["steampowered"]["url_search"])
    deferred.addCallback(return_spider_output)

    return deferred

def return_spider_output(output):
    _encoder = ScrapyJSONEncoder(ensure_ascii=False)
    return _encoder.encode(output)

app.run("localhost", 8080)
