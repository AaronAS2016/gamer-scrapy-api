# Instalar dependecias

```pip install -r requirements.txt```

# Levantar API Klein

``` python app.py ```

# Acceder a la API

## URL

ingresar en el navegador con los valores correspondientes

``` http://localhost:8080/search/[modo]/[orden]/[query][filtro] ```

| Parametro | Tipo | Descripcion |
| :--- | :--- | :--- |
| `modo` | `string` | Modo de busqueda de la frase dada en `[query]` |
| `orden` | `string` | Orden en el que se van a mostrar los resultados |
| `query` | `string` | Palabra/frase a buscar |
| `filtro` | `string` | FIltros que se usaran en los resultados |

### [modo] **Obligatorio**

| Parametro | Descripcion |
| :--- | :--- |
| `exacta` | Busca que este exactamente la frase dada en [query] |
| `todas_palabras` | Busca los resultados que contengan la frase dada en [query] |
| `algunas_palabras` | Busca que contenga por lo menos una palabra de frase dada en [query] |

### [orden] **Obligatorio**

| Parametro | Descripcion |
| :--- | :--- |
| `nombre_asc` | Ordena los titulos de la A a la Z |
| `nombre_desc` | Ordena los titulos de la Z a la A |
| `relevancia` | Busca los resultados que contengan la frase dada en [query] |
| `precio_asc` | Ordena los precios de menor a mayor |
| `precio_desc` | Ordena los precios de mayor a menor |

### [query] **Obligatorio**

Es la palabra o frase a buscar. Reemplazar los espacios por %20.
Ejemplo ```metro%20exodus```

### [filtro]
| Parametro | Descripcion |
| :--- | :--- |
| `filtro=[proveedor]`* | Elimina el proveedor dado |
| `filtro=[precio_minimo]&filtro=[precio_maximo]` | toma los titulos con los precios que esten dentro de ese rango |

*Trabajamos con 4 proveedores: ```gamesplanet```, ```gog```, ```nuuvem``` y ```steampowered```

Ejemplo: ```?filtro=gog&rango=0&rango=20```

###Ejemplo :
```http://localhost:8080/search/exacta/nombre_asc/metro?filtro=gog&rango=0&rango=20```
