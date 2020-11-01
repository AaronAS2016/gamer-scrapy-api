import crochet
crochet.setup()

from flask import Flask, request, jsonify
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from config.config import SITES_TO_SEARCH
from config.sites import CONFIG_SITE
import time

from storescraping.spiders.steam import SteamSpider
from storescraping.spiders.store import StoreSpider
from storescraping.spiders.test import TestSpider

app =  Flask(__name__)

output_data = []
crawl_runner = CrawlerRunner()

@app.route("/scrape/<modo>/<query>/")
def scrapear(modo, query):
    scrape_with_crochet(modo, query)

    time.sleep(20)

    return jsonify(output_data)

@crochet.run_in_reactor
def scrape_with_crochet(modo, query):

    dispatcher.connect(_crawler_result, signal=signals.item_scraped)

    for site in SITES_TO_SEARCH:
        if site == "test":
            crawl_runner.crawl(TestSpider)
        elif site == "steampowered":
            crawl_runner.crawl(SteamSpider, modo=modo, query=query, url_search=CONFIG_SITE[site]["url_search"])
        else: 
            crawl_runner.crawl(StoreSpider, modo=modo, query=query, config=CONFIG_SITE, sites_to_search=SITES_TO_SEARCH)

def _crawler_result(item, response, spider):
    output_data.append(dict(item))