import scrapy


class TestSpider(scrapy.Spider):
    name = "test"
    start_urls = [
        "https://en.wikipedia.org/wiki/Ricardo_Fort"
    ]

    def parse(self, response):
        text = response.xpath(
            "//h1[@id='firstHeading']/text()").get()
        yield {
            "comandante": text
        }