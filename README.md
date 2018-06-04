**Este Archivo README.md y el repositorio en general se encuentran en construcción**

Este es un repositorio con nuestro proyecto realizado para el Hackatón de *New Creativity 2018*, que tuvo como tema principal la creatividad literaria. El proyecto consistió en una especie de chatbot, que se entrena sobre algún texto (de preferencia algun texto literario notable, como una novela o un libro de poemas), e interactúa con el usuario para crear un texto orginal.

El entrenamiento del bot consiste en construir cadenas de markov a partir del texto original, una cadena captura la secuencia de palabras (utilizada para generar el texto), y otra cadena captura la secuencia de las estructuras gramaticales del autor. Una vez que interactúa con el usuario, el programa toma la última palabra del usuario, revisa su categoría gramatical, y propone una siguiente palabra que pertenezca al vocabulario del texto original, y cuya categoría gramatical sea coherente con la última ingresada por el usuario. Posteriormente, se usa esta palabra como semilla para que el bot genere una respuesta.

En este repositorio también se presentan diferentes "demos" que muestran la versatilidad de nuestro programa. En *demo1.py* se ejemplifica el uso básico del chatbot. En *demo2.py* se presenta una variación donde el bot también va aprendiendo el lenguaje del usuario y lo va combinando con su entrenamiento previo con el texto. Y en *demo3.py* se muestra un caso donde se entrenan a dos bots, sobre dos textos distintos, y se ponen a conversar entre ellos, sin que haya interacción del usuario. También se incluirá un programa que permita lanzar al bot a twitter, y que interactuará con los usuarios a través de tweets.

En *tutorial.py* se encuentra una explicación paso a paso de cómo utilizar nuestros modulos para poder programar aún más variaciones que las presentadas en los demos. Sin embargo, para usar los demos no es necesario entender el *tutorial.py*, solo es necesario correr los scripts (seguir leyendo esta guía).

# Instalación
Los programas están hechos con Python 3.5+. Entre los requerimientos se encuentra numpy y nltk, y sus respectivas dependencias.

# Textos de entrada
Es necesario proveer un archivo de texto plano .txt para entrenar a un bot. Se prefiere un texto largo como una novela, o un compendio de poemas, para que el entrenamiento sea adecuado. Aunque se prefiere que el archivo de entrada tenga un párrafo por cada línea, separados por saltos de línea, se esperaría que funcionara con cualquier archivo de texto plano.

Se recomienda poner a los archivos de texto dentro de la carpeta "textos" de este repositorio para mantener cierto orden, sin embargo no es obligatorio. El repositorio ya incluye unos archivos de texto: *suenio.txt* (que contiene el Primero Sueño de Sor Juana Inés de la Cruz) y *lovecraft.txt* (que contiene la novela The Dunwich Horror de H.P. Lovecraft) y *prueba_corta.txt* que tiene un texto genérico para hacer pruebas. Los tres están libres de derechos de autor.

# Demos con los textos incluidos en el repo
Los demos trabajan por default con los textos incluidos en el repositorio. Sin embargo, es necesario generar archivos intermedios utilizando dichos textos. Para ello, simplemente correr los siguientes tres comandos:

```
$ python3 texto_a_archivos.py suenio
$ python3 texto_a_archivos.py lovecraft
$ python3 texto_a_archivos.py prueba_corta
```

Estos crean la carpeta "./generados/" y diversos archivos necesarios para que los bots funcionen con los textos mencionados. Más adelante se explican estos archivos generados.

Una vez hecho lo anterior, se puede correr cualquiera de los tres demos usando:

```
$ python3 demo1.py
```

A continuación se explica lo que hace cada demo:
* *demo1.py* - Se ejecuta un chatbot entrenado con suenio.txt para interactuar con el usuario. El programa inicia, se espera la respuesta del usuario, y luego el programa responde.
* *demo2.py* - Se ejecuta un chatbot entrenado con prueba_corta.txt para interactur con el usuario. Funciona igual que *demo1.py*, pero aprende el lenguaje del usuario al reentrenar la cadena de markov con cada input del usuario.
* *demo3.py* - Se entrenan dos bots, uno con el suenio.txt y otro con lovecraft.txt, y se ponen a interactuar entre ellos. El usuario debe apretar "enter" para que la interacción avance.

Los tres demos terminan cuando el usuario oprime "Ctrl + C"

# Archivos generados
Como se ha mencionado, es necesario generar archivos a partir de los textos para que los bots funcionen. Para automatizar el proceso se ha creado el script *texto_a_archivos.py* ya mencionado. Dicho script recibe como argumento el nombre del texto y genera automáticamente los archivos relevantes en la carpeta *./generados/*. Su uso es el siguiente:

```
$ python3 texto_a_archivos.py nombre
```

Donde "nombre" es el nombre del archivo "nombre.txt" que **debe** encontrarse en el directorio "./textos". Atención: al invocar el script NO se debe incluir la extensión ".txt" del archivo.

En general, se pueden ignorar estos archivos, pues son para el funcionamiento interno del bot. Para aprender más sobre ellos, se podría revisar el *tutorial.py* o la documentación de los programas.

Para tener una breve idea de lo que son, a continuación se enlistan:
* *nombre.categ.txt* - archivo de texto que contiene la secuencia de categorías gramaticales detectadas en *nombre.txt*
* *nombre.dic.pickle* - archivo binario que contiene el diccionario categoría gramatical-palabras creado con *nombre.txt*
* *nombre.markov-generador.pickle* - archivo binario que contiene la cadena de markov para generar texto
* *nombre.markov-gramatical.pickle* - archivo binario que contiene la cadena de markov para escoger categorías gramaticales, creado con *nombre.txt*.

La razón para tener estos archivos en disco, es para ahorrar tiempo de entrenamiento y para que se pueda acceder directamente a estos archivos y explorar en caso de falla.

# Demos con textos del usuario
Los scripts de los demos pueden trabajar con textos provistos por el mismo usuario.

Lo primero es generar los archivos intermedios con los textos del usuario, usando el comando ya descrito:

```
$ python3 texto_a_archivos.py nombre
```

Luego se pasa el "nombre" como argumento para los demos para utilizarlos con el texto de los usuarios. Por ejemplo:

```
$ python3 demo1.py nombre
```

y

```
$ python3 demo2.py nombre
```

Para chatear con bots entrenados con *nombre.txt*

Y se usa

```
$ python3 demo3.py nombre1 nombre2
```

Para ver a el chat entre los bots entrenados con *nombre1.txt* y *nombre2.txt* respectivamente.

**Nota**: Los nombres pasados como argumentos a los scripts no deben llevar la extensión ".txt".
**Nota**: En caso de disponer de un nombre, cuyos archivos no se encuentren en *./generados/*, sucederán errores.
**Nota**: En caso de no pasar un "nombre" como argumento, simplemente se usarán los archivos incluidos en el repositorio.

# Logs de los usuarios
Los demos registran todo lo ingresado por el usuario dentro de archivos de texto plano en la carpeta "./user_logs/" (que se crea automáticamente al ejecutar algún demo).

Para saber más sobre cómo se hace esto, ver los códigos de los demos, el *tutorial.py* o la documentación del código.

# Otras variaciones
Los modulos, y sus respectivos procedimientos y clases han sido creados para que tengan mucha flexibilidad a la hora de crear diferentes bots. Los *demos* son ejemplos inmediatos de uso, y el archivo *tutorial.py* explica como trabajar paso a paso con los diferentes elementos del repositorio.

Algunas variaciones que se podrían programar usando este repositorio son:

* En lugar de tener a dos bots interactuando entre sí, se podrían tener decenas de ellos y escoger aleatoriamente de quién será el turno de "escribir". Incluso se podría armar un juego, donde el usuario deba adivinar quién escribió qué (especialmente interesante si el usuario no conoce los textos que se usaron en el entrenamiento).

* Se puede combinar el demo2 y el demo3 para hacer que los bots del demo3 adquieran lenguaje el uno del otro, de tal manera que se termine con bots que tengan una interesante combinación de lenguajes. No es necesario ver las interacciones entre los bots, sino simplemente programar su interacción y luego revisar los resultados.

* En lugar de usar textos clásicos, se pueden entrenar a los bots con texto hechos por el propio usuario para capturar su lenguaje. También, de utilizarse durante mucho tiempo, se podrían usar los logs de los usuarios para entrenar bots.

* Se pueden crear bots que interactúen con alguna página de internet, por ejemplo con twitter.
