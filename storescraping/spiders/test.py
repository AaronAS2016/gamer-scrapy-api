import scrapy


class TestSpider(scrapy.Spider):
    name = "test"
    start_urls = [
        "https://en.wikipedia.org/wiki/Ricardo_Fort"
    ]

    def parse(self, response):
        text = response.xpath(
            "/html/body/div[3]/div[3]/div[5]/div[1]/p[1]").get()
        yield {
            "comandante": text
        }