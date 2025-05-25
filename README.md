# Sistema de Recomendación de Ítems (Libros, Películas y Videojuegos)

Este proyecto es un sistema de recomendación que permite recomendar libros, películas o videojuegos a los usuarios en función de diferentes algoritmos: recomendación simple (popularidad), colaborativa (similitud entre usuarios) y basada en contenido (similitud entre características de los ítems).

## Características principales

- **Carga y gestión eficiente de grandes datasets** de libros, películas y videojuegos.
- **Algoritmos de recomendación**:
  - Simple (basado en medias y popularidad)
  - Colaborativo (similitud entre usuarios)
  - Basado en contenido (similitud entre ítems por sus características)
- **Evaluación de las recomendaciones** mediante métricas como MAE y RMSE.
- **Interfaz por consola** para seleccionar usuario, tipo de recomendación y mostrar resultados.

---

## Estructura de carpetas y datasets

Para que el sistema funcione correctamente, debes descargar los datasets y colocarlos en la estructura de carpetas adecuada.  
A continuación se muestra cómo debe estar organizado el directorio del proyecto:

```
Proyecto/
│
├── dataset/
│   ├── MovieLens100k/
│   │   ├── movies.csv
│   │   └── ratings.csv
│   ├── Books/
│   │   ├── Books.csv
│   │   ├── Users.csv
│   │   └── Ratings.csv
│   └── VideoGames/
│       ├── meta_Video_Games.json.gz
│       └── Video_Games_5.json.gz
│
├── main.py
├── dataset.py
├── items.py
├── recomenador.py
├── user.py
├── avaluador.py
├── toolkit.py
└── ...
```

---

## Descarga de los datasets

### MovieLens 100k
- Descárgalo desde: [https://grouplens.org/datasets/movielens/100k/](https://grouplens.org/datasets/movielens/latest/)
- Extrae los archivos `movies.csv` y `ratings.csv` en la carpeta MovieLens100k.

### Books (Book-Crossing)
- Puedes encontrar el dataset en: [https://www2.informatik.uni-freiburg.de/~cziegler/BX/](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset)
- Coloca los archivos `Books.csv`, `Users.csv` y `Ratings.csv` en la carpeta Books.

### VideoGames (Amazon)
- Descarga los archivos de metadatos y ratings 5-core de videojuegos de Amazon desde: [https://nijianmo.github.io/amazon/index.html](https://nijianmo.github.io/amazon/index.html)
- Coloca `meta_Video_Games.json.gz` y `Video_Games_5.json.gz` en la carpeta VideoGames.

---

## Ejecución

1. Instala las dependencias necesarias (por ejemplo, numpy, gzip, etc.).
2. Ejecuta el programa principal:
   ```bash
   python main.py <dataset> <algorithm>
   ```
3. Sigue las instrucciones en pantalla para seleccionar usuario, tipo de recomendación y visualizar los resultados.

---

## Notas

- Si los archivos o carpetas no están en la ubicación correcta, el sistema mostrará errores de archivo no encontrado.
- Puedes modificar el número de ítems o usuarios cargados cambiando los límites en el código.
- El sistema está preparado para trabajar con grandes volúmenes de datos, pero la carga inicial puede tardar dependiendo del tamaño de los datasets.

---

¿Tienes dudas o sugerencias? ¡No dudes en abrir un issue o contactar con el autor!

