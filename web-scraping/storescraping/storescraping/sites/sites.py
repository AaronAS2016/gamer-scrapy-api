sites = {
    "steam": {
        "nice_name": "Steam",
        "url_base": "https://store.steampowered.com",
        "anti_scrapping": True,
        "uri_search": "/search/?term=[QUERY]",
        "parse_elements": {
            "items": {
                "type": "xpath",
                "selector": "//div[@id='search_resultsRows']/a"
            },
            "price": {
                "type": "css",
                "selector": ".search_price::text",
            },
            "title": {
                "type": "xpath",
                "selector": ".//span[@class='title']/text()"
            },
            "img_url": {
                "type": "xpath",
                "selector": ".//img/@src"
            },
        },
        "type": "infinite_scroll"
    },
    "epic": {
        "nice_name": "Epic Store",
        "url_base": "https://www.epicgames.com",
        "uri_search": "/store/es-ES/browse?pageSize=30&q=[QUERY]&sortBy=relevance&sortDir=DESC",
        "parse_elements": {
        },
        "type": "infinite_scroll"
    },

    "ps": {
        "nice_name": "Playstation Store",
        "url_base": "https://store.playstation.com/es-ar",
        "uri_search": "/search/[QUERY]",
        "parse_elements": {
        },
        "type": "infinite_scroll"
    }
}
