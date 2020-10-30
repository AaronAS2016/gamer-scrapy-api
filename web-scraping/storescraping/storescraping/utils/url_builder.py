def url_builder(site, sites_data, query_busqueda):
    site_data = sites_data[site]
    url_busqueda = site_data["url_base"] + site_data["uri_search"]
    url_busqueda = url_busqueda.replace("[QUERY]", query_busqueda)
    return url_busqueda

#FIX: hay que agregar los demas sitios y ver si refactorizamos para hacerlo mas clean.
def get_name_store(url):
    if url.find("steam"):
        return "steam" 


def get_site_data(url, sites_data):
    name_store = get_name_store(url)
    return sites_data[name_store]