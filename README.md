# keyWords

## Objetivo
El propósito de este proyecto es realizar una aplicación para la búsqueda de archivos por medio de palabras claves (keywords) donde se implemente un algoritmo óptimo para la analítica de texto.

## Prerrequisitos

* Python 3.6
* MongoDB
* MRJob
* NLTK
* Flask (Aplicación web)

## URL de Despliegue
```
http://10.131.137.172:5000
```
## Funcionamiento
Parcialmente el proyecto consta de dos elementos importantes:

* Una página web con un campo de texto para ingresar las palabras claves y un botón para iniciar la búsqueda de estas, la cual fue realizada en python con el framework flask. Aunque, actualmente esta no se encuentra integrada con la lógica.

* La lógica del proyecto, en este momento se encuentra dividida en tres archivos:

	* **inverted_index.py:** En este archivo es donde está todo el preprocesamiento de los datos, lo primero que se realiza es la separación de las palabras de los diferentes textos (tokenization), posteriormente se realiza la normalización de estas, es decir, eliminación de "stopwords", signos de puntuación y buscar el prefijo de estas. Finalmente, luego de realizar estas operaciones sobre los datos, se procede a insertar los mismos en la base de datos, donde el "id" definido es cada palabra y el contenido los archivos en donde aparece, con su respectiva frecuencia. Cabe aclarar que la realización de este proceso se hace por medio de Map/Reduce utilizando MRJob.
	* **mongo.py:** El fichero contiene una clase, llamada Mongo, encargada de inicializar y administrar la conexión con la base de datos. Adicionalmente, contiene dos funciones que abstraen las nociones de “inserción” y “búsqueda”:
La primera se encarga de formar un diccionario con el formato ```{"_id": <word>, "file_paths": <file_paths>})```, donde <file_paths> es una lista de tuplas, cada una con: Un string referente al documento donde se encuentra la palabra y un entero que simboliza la cantidad de ocurrencias de la palabra en dicho documento.
La segunda permite obtener la cantidad total de ocurrencias de una palabra en cada documento, al igual que el nombre del fichero en cuestión.


## Proceso de ETL

Para el proceso de ETL se debe ejecutar el siguiente comando, el cual se encargará de crear el índice invertido a partir del Map/Reduce realizado a los textos de entrada.

**1.** Ejecutar inverted_index.py para el pre-procesamiento de los datos y almacenarlos en la base de datos:

```
$ python3.5 inverted_index.py --python-bin /opt/python3/bin/python3.5 -r hadoop hdfs:////datasets/gutenberg/* --output hdfs:////user/<user>/<output_dir>
```
El fichero **inverted_index.py** está compuesto por 3 bloques principales, el primero de ellos es la clase Mongo desarrollada por nuestro equipo que fue incluida en este fichero, por facilidad al momento de ejecutar un solo fichero en la línea anterior. El segundo bloque es la función encargada de ***tokenizar*** las líneas de entrada y aplicar las transformaciones correspondientes sobre estas (***Stemming***, eliminar ***stopwords***). Por último el bloque 3 contiene la clase más importante, la cual es la encargada de ejecutar **Map/Reduce** a través de **MRJob**

A continuación se muestra un pseudocódigo de los algoritmos de este fichero:



```python
# Bloque 1
class Mongo()
    client = MongoClient(<MONGO_SERVER>, <MONGO_SERVER_PORT>)
    db = client[<DB_NAME>]
    db.authenticate(MONGO_USER, MONGO_PASS)
    <COLLECTION_NAME> = db[<COLLECTION_NAME>]

  function insert(self, word, file_paths)
    <COLLECTION_NAME>.insert_one({"_id": word, "file_paths": file_paths})

  function search(self, word)
    return <COLLECTION_NAME>.find_one({"_id": word})

# Bloque 2
function tokenize(line, language)
  stemmed_words = []
  words = tokenizer.tokenize(line)
  if language == 'es', then
    for w in words, do
      if w not in spanish_stop_words, then
        stemmed_words.append(spanish_stemmer.stem(w))
  else
    for w in words, do
      if w not in english_stop_words, then
        stemmed_words.append(english_stemmer.stem(w))

  return stemmed_words

# Bloque 3
class InvertedIndex(MRJob)

  function mapper(_, line)
    line = deleteNumbers(line)
    if line != "", then
      file_name = getName('mapreduce_map_input_file)
      language = file_name.split('/')[-2]
      words = tokenize(line, language)
      for word in words, do
        emit (word, file_name),1

  function combiner(pair, values)
    emit pair[0], (pair[1], sum(values))

  function reducer(word, values)
    file_names, frec = zip(*values)
    result = dict(file_names)
    for file_name in values, do
      result[file_name[0]] += file_name[1]
    sorted_result = sorted(result, reverse=True)
    if len(sorted_result) > 10, then
      db.insert(word, sorted_result[:10])
    else
      db.insert(word, sorted_result)

    emit word, result
```
**2. controller.py:** Básicamente, en el controlador es donde se encuentra la función que es llamada desde la aplicación web cuando un usuario ingresa la frase a buscar. Esta función contiene toda la lógica de búsqueda, separación y normalización de la frase dada, además, se encarga de retornar los datos necesarios para listar en la aplicación web, arrojando como resultado los primeros diez documentos en orden con su respectiva frecuencia.

Para su implementación en python se utiliza la biblioteca NLTK, la cual ayuda en el procesamiento del texto, y se utiliza la clase Mongo (Realizada por el equipo) para hacer las diferentes búsquedas en la base de datos.

Pseudocódigo:
```python
function get_files(phrase, language):

  # Bloque 1
  stop_words = stopwords.words(language)
  stemmer = stemmer(language)
  tokenizer = tokenizer()
  splited_words = tokenizer.tokenize(phrase)

  # Bloque 2
  for word in splited_words:
    if word not in stop_words:
      word = stem(word)
      files = db.search(word)
      if files is not None:
        files = files['file_paths']
        for file in files:
          if file[0] not in dic:
            dic[file[0]] = file[1]
          else:
            dic[file[0]] += file[1]
  sorted_list = sorted(reverse(list(dic)))

  # Bloque 3
  if len(sorted_list) == 0:
    return (None,None)
  else:
    paths, freq = zip(*sorted_list)
    for file in sorted_list:
      path = file[0].split("/")
      language = path[-2]
      file_name = path[-1]
      address.append("http://10.131.137.188/{}/{}".format(language, file_name))
  return (tuple(address[:10]), freq[:10])
```
El pseudocódigo anterior recibe dos parámetros, la frase que se va a buscar y el idioma en el que esta fue escrito, este se divide en tres bloques fundamentales:

**Bloque 1:** Inicializar todas las herramientas necesarias para realizar la separación y normalización de la frase dada, como se puede observar en este caso se hace muy general, sin embargo, como se dijo anteriormente, python necesita de NLTK para realizar esto.

**Bloque 2:** Se realiza el procesamiento sobre cada una de las palabras dadas y se hace la búsqueda en la base de datos, cada vez que encuentre una instancia agrega a un diccionario donde la clave es el nombre del fichero actual y a su contenido le suma la frecuencia del documento actual, por tal el resultado final del diccionario será un conjunto de claves que representa a cada documento y un conjunto de valores que serán la frecuencia de aparición en dicho documento. Finalmente, el diccionario se convierte en una lista y se ordena de forma decreciente.

**Bloque 3:** En el último bloque lo que se hace es comprobar que el resultado de la lista sea diferente de nulo, y da un formato a lo que debe retornar para que este sea listado correctamente en la aplicación web. Finalmente solo retorna los diez primeros elementos que son los únicos solicitados por la aplicación.

**3.** Finalmente para ver el contenido actual de la página web se puede realizar el siguiente comando y dirigirse a localhost:5000
```
$ python run.py
```




