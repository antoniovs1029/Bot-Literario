import nltk
import re
import os.path
import os
from nltk.corpus import stopwords
from collections import defaultdict
from random import choice, randint
from re import findall
import pickle

def generar_archivos_ct_y_dic(ruta_texto, ruta_categtxt, ruta_dic, forzar = False):
    """
    Construye el archivo de las categorias gramaticales del texto de entrada
    y el diccionario que asocia las palabras de dicho texto con su respectiva
    categoría gramatical.

    El archivo de categorias gramaticales es un simple archivo de texto que en lugar de tener
    las palabras del archivo de texto de entrada, tiene sus categorias gramaticales.

    El archivo de diccionario es un binario creado a partir de un defaultdict de python
    donde las llaves son cadenas de categorías gramaticales y los valores son listas de palabras
    asociadas con dicha categoría.

    Dichos archivos tendrán la extensión .categ.txt y .dic.pickle respectivamente,
    y se pondrán en la misma carpeta donde esté el texto de entrada, y tendrán
    el mismo nombre que dicho texto.

    :param: ruta_texto: string de la ruta donde se encuentra el texto de entrada
    :param: ruta_categtxt: string de la ruta donde se pondrá el texto convertido a categorias.
    :param: ruta_dic: string de la ruta donde se pondrá el diccionario categorías-palabras
    :param: forzar: booleano. Si es falso, omite volver a crear los archivos si ya existen. Si es verdadero, obliga a volver a crearlos aun cuando existan 
    :return: No regresa nada
    """
    
    nombre_texto = os.path.basename(ruta_texto) # solo el nombre del archivo

    if not os.path.exists(ruta_texto):
        print("Error: El archivo", ruta_texto, " no existe")
        exit()

    if not forzar and os.path.exists(ruta_categtxt) and os.path.exists(ruta_dic):
        print("Los archivos de estructuras gramaticales de", nombre_texto, "ya existen en la ruta indicada. No se crearan de nuevo")
        return

    print("Creando los archivos de estructuras gramaticales de", nombre_texto)

    diccionario = defaultdict(list)
    with open(ruta_categtxt, "w") as categf:
        with open(ruta_texto, 'r') as txtf:
            for linea in txtf:
                if len(linea) != 1:
                    pos = nltk.pos_tag(nltk.word_tokenize(linea))
                    # pos es PartOfSpeech, es una lista de tuplas
                    # ('palabra', 'CATEGORIA') para cada palabra de la linea

                    for palabra, categoria in pos:
                        categf.write(categoria + " ")
                        if palabra not in diccionario[categoria]:
                            diccionario[categoria].append(palabra)
                else:
                    categf.write("\n")
    pickle.dump(diccionario, open(ruta_dic, "wb"))
    return

class DiccionarioGramatical:
    """
    Contiene un diccionario que asocia categorías gramaticales a palabras.
    Tiene un defaultdic llamado "diccionario" donde las llaves son cadenas
    de categorías gramaticales y los valores son listas de palabras
    asociadas con dicha categoría.
    """
    def __init__(self):
        """
        Inicializador de DiccionarioGramatical
        """
        self._diccionario = defaultdict(list)

    def cargar(self, ruta_dic):
        self._diccionario = pickle.load(open(ruta_dic,"rb"))

    def existe_categoria(self, categoria):
        return categoria.upper() in self._diccionario.keys()

    def escoger_palabra_de_categoria(self, categoria):
        """
        Se escoge una palabra de cierta categoría, a partir de un diccionario de categorías-palabras.
        Si la categoria ingresada no existe, se regresa una palabra aleatoria.
        :param: diccionario: diccionario de categorías-palabras
        :param: categoria: categoria con la cual seleccionar
        :return: palabra de dicha categoria. Si la categoria no existe en el diccionario, se regresa una palabra del diccionario al azar.
        """
        if len(self._diccionario.keys()) == 0:
            print("El diccionario esta vacio")
            return

        if not self.existe_categoria(categoria):
            categoria = choice(list(self._diccionario.keys())) 
        
        return choice(self._diccionario[categoria.upper()]) #las categorias en el diccionario suelen estar en mayusculas    

class MarkovGramatical:
    """
    Cadena de Markov que analiza la secuencia de categorias gramaticales de un texto.
    Permite elegir una categoria gramatical siguiente a partir de una categoria gramatical dada.
    """
    def __init__(self):
        """
        Inicializador de MarkovGramatical

        :param: ruta_categtxt: ruta donde se encuentra el archivo de las categorias del texto
        :ventana: cuantas palabras hacia atrás condicionan la cadena
        :return: No regresa nada
        """
        self._markov = defaultdict(list)


    def entrenar(self, ruta_categtxt, ventana = 1):
        """
        Entrena la cadena de markov con un archivo de categorías gramaticales.
        Borra la cadena existente para crear una nueva.
        
        :param: ruta_categtxt: string con la ruta con el archivo para entrenar
        :param: ventana: int de cuántas palabras hacia atrás condicionan la cadena. Opcional. El default es 1.
        :return: No regresa nada
        """
        self._markov = defaultdict(list)
        text = open(ruta_categtxt).read()
        words = findall("[A-Z']+", text.upper()) # debido a esto, las categorias se guardaran en mayusculas en la cadena de markov
        #TODO: ver una mejor manera de crear la cadena de markov gramatical sin usar la anterior expresion regular
        # ya que hay varias cosas que se pierden, como por ejemplo, existe la categoria gramatical "PRP$" que deja de
        # existir al usar ese regex, y luego traer problemas al obtener la categoria gramatical ingresada por el usuario.
        for i in range(len(words) - ventana):
            self._markov[tuple(words[i:i + ventana])].append(words[i + ventana])

    def guardar(self, ruta_markov_gramatical):
        """
        Guarda la cadena de markov en un binario usando pickle en la carpeta de "entradas".
        El nombre será el nombre del archivo en el que se basa, y la extensión será ".markov-gramatical.pickle".
        
        :param: ruta_markov-gramatical: ruta donde se guardara la cadena de markov
        :return: No regresa nada
        """
        pickle.dump(self._markov, open(ruta_markov_gramatical, "wb"))

    def cargar(self, ruta_markov_gramatical):
        """
        Carga un archivo binario (previamente hecho con pickle) que contiene una cadena de markov.
        Se asigna dicha cadena de markov al objeto MarkovGramatical actual.
        
        :param: ruta_markov-gramatical: ruta donde se encuentra la cadena de markov a cargar
        :return: No regresa nada
        """
        self._markov = pickle.load(open(ruta_markov_gramatical, "rb"))

    def existe_categoria(self, categoria):
        return (categoria,) in self._markov.keys()

    def obtener_siguiente_categoria(self, categoria_anterior):
        """
        Escoge una categoria siguiente dependiendo la categoria anterior. Si la categoria anterior
        no se encuentra en la cadena de markov, entonces escoge al azar.
        :param: categoria_anterior: string con el nombre de la categoria anterior (ejem. 'nn')
        :return: string con el nombre de la categoria siguiente escogida
        """
        if not self.existe_categoria(categoria_anterior):
            categoria_anterior = choice(list(self._markov.keys()))[0] # se debe quitar de la tupla
        return choice(self._markov[categoria_anterior,]).upper() # es necesaria la coma, pues se guardan como tuplas. ejem: ('nn',).
                                                                # es necesario el .upper() pues en la cadena de markov se guardaron como mayusculas

