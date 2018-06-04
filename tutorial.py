#!/usr/bin/env python3

"""
En este tutorial se muestra la manera de utilizar los modulos provistos en este proyecto
para terminar con el chat interactivo. Los modulos a utilizar son "gramatical" "generacion" y "otros".

En general, lo que hace el programa es entrenar cadenas de markov a partir de un texto;
una captura el vocabulario y la secuencia de palabras, mientras que otra captura la secuencia
de categorías gramaticales. También se crea un diccionario categoría-palabra a partir de dicho texto.

Luego, el programa genera un texto y se espera la respuesta del usuario. De dicha respuesta, se toma
solamente la ultima palabra, y se obtiene su categoría gramatical, luego se usa la cadena de markov
de categorías gramaticales para obtener una siguiente categoría gramatical. Con el diccionario ya creado
se obtiene una palabra correspondiente a dicha categoria, y se usa esa palabra para iniciar la generación
de la respuesta de la computadora. La interaccion continua indefinidamente hasta que el usuario oprime
"Ctrl + C".

El tutorial se encuentra dividido en pasos, los pasos 0, 1 y 2 son para generar las cadenas de markov y el
diccionario. Estos son guardados en disco con las extensiones .markov-gramatical.pickle .markov-generador.pickle
y .dic.pickle. Una vez creados estos archivos, ya no es necesario crearlos otra vez; por lo que, generalmente,
se omitirán estos pasos y simplemente se cargaran los archivos .pickle para crear los objetos correspondientes.

Finalmente, la interacción del usuario es guardada en un archivo de texto plano. 
"""

from modulos.gramatical import generar_archivos_ct_y_dic, MarkovGramatical, DiccionarioGramatical
from modulos.generacion import MarkovGenerador
from modulos.otros import user_input, crear_dir
from nltk import pos_tag
import os

###############################################################################
# PASO 0: Determinar las rutas del texto de entrada y las rutas de los archivos
# que se generaran. Se usa el modulo "os" para crear las rutas, para asi evitar
# problemas si se corre en diferentes sistemas operativos.

# Archivo de texto en ./textos/:
nombre = "lovecraft"
ruta_texto = os.path.join(".", "textos", nombre + ".txt") # "./textos/lovecraft.txt"

# Archivos que se generarán en el demo:
# ./generados/lovecraft.categ.txt - texto convertido a categorías gramaticales
# ./generados/lovecraft.dic.pickle - diccionario categorías-palabras
# ./generados/lovecraft.markov-gramatical.pickle - cadena de markov de estructuras gramaticales
# ./generados/lovecraft.markov-generador.pickle - cadena de markov que genera texto
# ./user_logs/tutorial.lovecraft.userlog.txt - log de lo que el usuario pone (podria ser util para entrenar nuevas cadenas)

dir_generados = os.path.join(".", "generados") # "./generados/"
crear_dir(dir_generados) # Se crea ./generados/ si no existe
ruta_categtxt = os.path.join(dir_generados, nombre + ".categ.txt") 
ruta_dic = os.path.join(dir_generados, nombre + ".dic.pickle")
ruta_markov_gramatical = os.path.join(dir_generados, nombre + ".markov-gramatical.pickle")
ruta_markov_generador = os.path.join(dir_generados, nombre + ".markov-generador.pickle")

dir_user_logs = os.path.join(".", "user_logs")
crear_dir(dir_user_logs)
ruta_log_user = os.path.join(dir_user_logs, "tutorial." + nombre + ".userlog.txt")

###############################################################################
# PASO 1: Análsis de estructuras gramaticales
# Creacion de archivo de texto de categorias gramaticales y diccionario
# (lovecraft.categ.txt y lovecraft.dic.pickle)
generar_archivos_ct_y_dic(ruta_texto, ruta_categtxt, ruta_dic)
diccionario = DiccionarioGramatical()
diccionario.cargar(ruta_dic)

# Creación de la cadena de markov gramatical:
mgram = MarkovGramatical()
mgram.entrenar(ruta_categtxt)
mgram.guardar(ruta_markov_gramatical) # backup, no es necesario


###############################################################################
# PASO 2: Crear cadena de markov que generará texto
mgen = MarkovGenerador()
mgen.entrenar(ruta_texto)
mgen.guardar(ruta_markov_generador)

###############################################################################
# Paso 3: Interactuar
print("\n----Se Inicia el Chat con", nombre + ".txt", "------\n")
print(mgen.generar_texto()) # el programa inicia generando texto
terminar = False
while not terminar:
    try:
        entrada = user_input(ruta_log = ruta_log_user) # se recibe la entrada del usuario y se registra en un log
    except KeyboardInterrupt: # Si se oprime Ctrl + C se acaba la interaccion
        terminar = True 
        print("----- FIN ------")
    else:
        ultima_palabra = entrada.split(' ')[-1] # la ultima plabra ingresada por el usuario
        ultima_categoria = pos_tag([ultima_palabra])[0][1] #la categoria gramatical de dicha palabra. Recordar que pos_tag devuelve una lista de tuplas donde el segundo elemento es la categoria
        siguiente_categoria = mgram.obtener_siguiente_categoria(ultima_categoria) # escoger la siguiente categoria usar, a partir de la ultima
        siguiente_palabra = diccionario.escoger_palabra_de_categoria(siguiente_categoria) # escoger la siguiente palabra, a partir de la categoria seleccionada
        print(mgen.generar_texto(siguiente_palabra)) # generar mas texto a partir de la palabra seleccionada

