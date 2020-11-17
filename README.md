# Troya-Mosaic
Procesamiento de imágenes para generar mosaicos de fotos.

Funcionamiento actual del software:
Foto Original            |  Procesada (Average)
:-------------------------:|:-------------------------:
<img src="images/troyita.png" width="350"/>  |  <img src="results/average/average.jpg" width="350"/>

### Funcionamiento
El programa toma todas las imágenes que se vayan a utilizar para el mosaico y se calcula el color más común de cada una de ellas. Tras ello, se divide la imagen principal en el número *azulejos* que se quieran; se irá calculando el color más común en cada uno de esos *azulejos* y se reemplazarán por la imagen que más se acerque en color.

Para calcular el color más común se pueden utilizar tres métodos distintos:
- *Average*: obtiene el color más común calculando la media de todos los píxeles.
- *PixelCount*: cuenta el número de repeticiones de cada píxel y se queda con el color que más se repita. Puede controlarse la variabilidad de color con el parámetro `redu`.
- *AveragePixelCount*: calcula la media de los *n* colores que más se repitan utilizando *PixelCount*.
- *KMeans*: calcula los colores más comunes utilizando clustering (demasiado lento).

Las imágenes de los resultados que se encuentran en este repositorio están bastante comprimidas. El programa puede guardar la imagen con el tamaño deseado.
