def sort_data(data, sort_type, index, query):
    data_sorted = []
    apply_order = index == "desc"
    if sort_type == "nombre":
        data_sorted = sorted(
            data, key=lambda x: x["title"], reverse=apply_order)
    elif sort_type == "relevancia":
        data_sorted = sorted(data, key=lambda x: x["price"])
        data_sorted = sort_by_relevance(data, query)
    elif sort_type == "precio":
        data_sorted = sorted(
            data, key=lambda x: x["price"], reverse=apply_order)
    return data_sorted


def sort_by_relevance(data, query):
    array_busqueda = [(0, resultado) for resultado in data]
    sorted_por_peso = []

    for peso, resultado in array_busqueda:
        titulo = resultado["title"].lower()
        primer_palabra = titulo.split(" ")[0]
        if primer_palabra == "metro":
            peso +=3
        if primer_palabra.startswith(query.lower()):
            peso += 2
        if query.lower() in titulo: 
            peso += 1

        sorted_por_peso.append((peso, resultado))

    sorted_por_peso = sorted(sorted_por_peso, key=lambda x: x[0], reverse=True)

    return [resultado for peso, resultado in sorted_por_peso]
