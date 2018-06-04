from collections import defaultdict
from random import choice, randint
from re import findall
import numpy as np
import pickle

class MarkovGenerador:
    def __init__(self):
        self._markov = defaultdict(list)
        self._palabras = [] # el texto de entrenamiento, pero expresado como lista de palabras
                            # si el texto es demasiado grande podrian haber problemas con la generacion de textos
                            # y quizas se tenga que cambiar esta implementacion para que no requiera guardar el texto en memoria

        self._ventana = 2 # numero de palabras con las cuales se condiciona la cadena. La implementacion actual solo funciona con 2.

    def entrenar(self, ruta_texto):
        self._markov = defaultdict(list)
        self.reentrenar(ruta_texto)
    
    def reentrenar(self, ruta_texto):
        with open(ruta_texto) as txtfile:
            text = txtfile.read()    
            self.reentrenar_con_cadena(text)

    def reentrenar_con_cadena(self, cadena):
        self._palabras += findall("[a-z'áéíóúñ]+", cadena.lower())
        for i in range(len(self._palabras) - self._ventana):
            self._markov[tuple(self._palabras[i:i + self._ventana])].append(self._palabras[i + self._ventana])       
                 
            
    def guardar(self, ruta_guardar):
        pickle.dump((self._markov, self._palabras), open(ruta_guardar, "wb"))

    def cargar(self, ruta_cargar):
        self._markov, self._palabras = pickle.load(open(ruta_cargar, "rb"))

    def generar_texto(self, primera_palabra = None, tamanio = None):
        if len(self._palabras) < self._ventana:
            print("No se puede generar texto, pues no hay palabras suficiente. Intente entrenar la cadena")
            return ""

        if tamanio == None:
            tamanio = randint(8,17)

        if primera_palabra == None:
            indice_semilla = randint(0, len(self._palabras) - self._ventana)
        else:
            indices_posibles = np.where(np.array(self._palabras) == primera_palabra)[0]
            if len(indices_posibles) > 0:
                indice_semilla = choice(indices_posibles)
            else:
                indice_semilla = randint(0, len(self._palabras) - self._ventana)
        
        generado = self._palabras[indice_semilla:indice_semilla + self._ventana]
        for _ in range(tamanio):
            posibles = self._markov[tuple(generado[-self._ventana:])]
            if len(posibles) > 0:
                generado.append(choice(posibles))        
            else: # Si por alguna razon la cadena de markov ya no puede continuar, se añade una palabra al azar y se termina la generacion
                azar = randint(0, len(self._palabras))
                generado.append(self._palabras[azar])
                break
        return ' '.join(generado)
