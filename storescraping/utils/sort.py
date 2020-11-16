def sort_data(data, sort_type, index):
    data_sorted = []
    apply_order = index=="desc"
    if sort_type == "nombre":
        data_sorted = sorted(data, key=lambda x: x["title"], reverse=apply_order)
    elif sort_type == "pagina":
        data_sorted = sorted(data, key=lambda x: x["provider"], reverse=apply_order)
    elif sort_type == "precio":
        data_sorted = sorted(data, key=lambda x: x["price"], reverse=apply_order)
    return data_sorted
