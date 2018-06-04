#!/usr/bin/env python3

"""
Se entrenan dos chatbots y se ponen a interactuar entre ellos.
"""

from modulos.gramatical import generar_archivos_ct_y_dic, MarkovGramatical, DiccionarioGramatical
from modulos.generacion import MarkovGenerador
from modulos.otros import user_input, crear_dir
from nltk import pos_tag
import os
import sys

if len(sys.argv) == 3:
    nombre1 = sys.argv[1]
    nombre2 = sys.argv[2]
else:
    # por default se cargara el archivo de "prueba_corta.txt"
    nombre1 = "lovecraft"
    nombre2 = "suenio"

print("Se cargara ./textos/" + nombre1 + ".txt")
print("Se cargara ./textos/" + nombre2 + ".txt")

dir_generados = os.path.join(".", "generados")
ruta_dic1 = os.path.join(dir_generados, nombre1 + ".dic.pickle")
ruta_markov_gramatical1 = os.path.join(dir_generados, nombre1 + ".markov-gramatical.pickle")
ruta_markov_generador1 = os.path.join(dir_generados, nombre1 + ".markov-generador.pickle")

ruta_dic2 = os.path.join(dir_generados, nombre2 + ".dic.pickle")
ruta_markov_gramatical2 = os.path.join(dir_generados, nombre2 + ".markov-gramatical.pickle")
ruta_markov_generador2 = os.path.join(dir_generados, nombre2 + ".markov-generador.pickle")

dir_user_logs = os.path.join(".", "user_logs")
ruta_log_user1 = os.path.join(dir_user_logs, "demo3." + nombre1 + ".userlog.txt")
ruta_log_user2 = os.path.join(dir_user_logs, "demo3." + nombre2 + ".userlog.txt")

diccionario1 = DiccionarioGramatical()
mgram1 = MarkovGramatical()
mgen1 = MarkovGenerador()
diccionario1.cargar(ruta_dic1)
mgram1.cargar(ruta_markov_gramatical1)
mgen1.cargar(ruta_markov_generador1)

diccionario2 = DiccionarioGramatical()
mgram2 = MarkovGramatical()
mgen2 = MarkovGenerador()
diccionario2.cargar(ruta_dic2)
mgram2.cargar(ruta_markov_gramatical2)
mgen2.cargar(ruta_markov_generador2)

print("\n----Se Inicia el Chat entre", nombre1 + ".txt y " + nombre2 + ".txt", "------\n")
texto1 = mgen1.generar_texto() 
terminar = False
while not terminar:
    print(nombre1 + ": " + texto1)

    ultima_palabra = texto1.split(' ')[-1]
    ultima_categoria = pos_tag([ultima_palabra])[0][1]
    siguiente_categoria = mgram2.obtener_siguiente_categoria(ultima_categoria)
    siguiente_palabra = diccionario2.escoger_palabra_de_categoria(siguiente_categoria)
    
    texto2 = mgen2.generar_texto(siguiente_palabra)
    print(nombre2 + ": " + texto2)

    ultima_palabra = texto2.split(' ')[-1]
    ultima_categoria = pos_tag([ultima_palabra])[0][1]
    siguiente_categoria = mgram1.obtener_siguiente_categoria(ultima_categoria)
    siguiente_palabra = diccionario1.escoger_palabra_de_categoria(siguiente_categoria)
    
    texto1 = mgen1.generar_texto(siguiente_palabra)    

    try:
        espera = input()
    except KeyboardInterrupt:
        terminar = True 
        print("\n----- FIN ------")
