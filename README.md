# Instalar dependecias

```pip install -r requirements.txt```

# Levantar API Klein

``` python app.py ```

# Acceder a la API


### modos
BUSQUEDA_EXACTA = "exacta"
BUSQUEDA_QUE_CONTENTA_TODAS_PALABRAS = "todas_palabras"
BUSQUEDA_QUE_CONTENGA_ALGUNAS_PALABRAS = "algunas_palabras"

``` http://localhost:8080/search/[modo]/[query] ```