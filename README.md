# Troya-Mosaic
Procesamiento de imágenes para generar mosaicos de fotos.

Uso del programa:

`python3 run.py <img_principal> <directorio_mosaicos> <n_imgs_col> <ancho_result> <nombre_result>`

Funcionamiento actual del software (*haga click sobre la imagen para poder diferenciar el mosaico*):
Foto Original            |  Procesada (20 imágenes, 100 mosaicos por columna) | Overlay (`alpha`=0.25)
:-------------------------:|:-------------------------:|:-------------------------:
<img src="images/flores.png" width="350"/>  |  <img src="results/average/flores_average_100.jpg" width="350"/>  |  <img src="results/average/flores_average_100.jpg_overlay.jpg" width="350"/>
<img src="images/troyita_buenasnoches.png" width="350"/>  |  <img src="results/average/troyita_buenasnoches_average_100.jpg" width="350"/>  |  <img src="results/average/troyita_buenasnoches_average_100.jpg_overlay.jpg" width="350"/>

### Funcionamiento
El programa toma todas las imágenes que se vayan a utilizar para el mosaico y se calcula el color más común de cada una de ellas. Tras ello, se divide la imagen principal en el número *azulejos* que se quieran; se irá calculando el color más común en cada uno de esos *azulejos* y se reemplazarán por la imagen que más se acerque en color.

Para calcular el color más común se han desarrollado cuatro métodos distintos:
- *Average*: obtiene el color más común calculando la media de todos los píxeles.
- *PixelCount*: cuenta el número de repeticiones de cada píxel y se queda con el color que más se repita. Puede controlarse la variabilidad de color con el parámetro `redu`.
- *AveragePixelCount*: calcula la media de los *n* colores que más se repitan utilizando *PixelCount*.
- *KMeans*: calcula los colores más comunes utilizando clustering (demasiado lento).

También se ha implementado un método que compara las imágenes píxel a píxel, pero es bastante ineficiente.

Los mejores resultados, por ahora, se obtienen con *Average*, con bastante diferencia al resto. Además, este es el método más rápido de todos los desarrollados.

Las imágenes de los resultados que se encuentran en este repositorio están bastante comprimidas. El programa puede guardar la imagen con el tamaño deseado.
