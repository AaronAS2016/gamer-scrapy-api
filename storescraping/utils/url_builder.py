def url_builder(site, sites_data, query_busqueda):
    site_data = sites_data[site]
    url_busqueda =  site_data["url_search"].replace("[QUERY]", query_busqueda)
    return url_busqueda

def get_name_store(url):
    return url.split(".")[1]


def get_site_data(url, sites_data):
    name_store = get_name_store(url)
    return sites_data[name_store]