# keyWords

## Objetivo
El propósito de este proyecto es realizar una aplicación para la búsqueda de archivos por medio de palabras claves (keywords) donde se implemente un algoritmo óptimo para la analítica de texto.

## Prerrequisitos

* Python 3.6
* MongoDB
* MRJob
* NLTK
* Flask (Aplicación web)

## Funcionamiento
Parcialmente el proyecto consta de dos elementos importantes:

* Una página web con un campo de texto para ingresar las palabras claves y un botón para iniciar la búsqueda de estas, la cual fue realizada en python con el framework flask. Aunque, actualmente esta no se encuentra integrada con la lógica.

* La lógica del proyecto, en este momento se encuentra dividida en tres archivos:

	* **inverted_index.py:** En este archivo es donde esta todo el preprocesamiento de los datos, lo primero que se realiza la separación de las palabras de los diferentes textos (tokenize), posteriormente se realiza la normalización de estas, es decir, eliminación de "stopwords", signos de puntación y buscar el prefijo de estas. Finalmente, luego de realizar estas operaciones sobre los datos, se procede a insertar estos en la base de datos, donde el "id" será cada palabra y el contenido será los archivos en donde aparece con su respectiva frecuencia. Cabe aclarar que la realización de este proceso se hace por medio de Map/Reduce utilizando MRJob.

## Proceso de ETL

Para el proceso de ETL se deben ejecutar el siguiente comando, el cual se encargará de crear el índice invertido a partir del Map/Reduce realizado a los textos de entrada.

1. Ejecutar inverted_index.py para el pre-procesamiento de los datos y almacenarlos en la base de datos:

```
$ python3.5 inverted_index.py --python-bin /opt/python3/bin/python3.5 -r hadoop hdfs:////datasets/gutenberg/* --output hdfs:////user/tllanos/out_gutenberg
```

3. Ingresamos a la ip 10.131.137.172:5000 Finalmente para ver el contenido actual de la página web se puede realizar el siguiente comando y dirigirse a localhost:5000
```
$ python run.py
```
