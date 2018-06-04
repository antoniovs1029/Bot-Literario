#!/usr/bin/env python3

"""
Se entrena un chatbot e interactua con el usuario. Aprende el lenguaje del usuario.
"""

from modulos.gramatical import generar_archivos_ct_y_dic, MarkovGramatical, DiccionarioGramatical
from modulos.generacion import MarkovGenerador
from modulos.otros import user_input, crear_dir
from nltk import pos_tag
import os
import sys

if len(sys.argv) == 2:
    nombre = sys.argv[1]
else:
    # por default se cargara el archivo de "prueba_corta.txt"
    nombre = "prueba_corta"

print("Se cargara ./textos/" + nombre + ".txt")

dir_generados = os.path.join(".", "generados")
ruta_dic = os.path.join(dir_generados, nombre + ".dic.pickle")
ruta_markov_gramatical = os.path.join(dir_generados, nombre + ".markov-gramatical.pickle")
ruta_markov_generador = os.path.join(dir_generados, nombre + ".markov-generador.pickle")

dir_user_logs = os.path.join(".", "user_logs")
ruta_log_user = os.path.join(dir_user_logs, "demo2." + nombre + ".userlog.txt")


diccionario = DiccionarioGramatical()
diccionario.cargar(ruta_dic)

mgram = MarkovGramatical()
mgram.cargar(ruta_markov_gramatical)

mgen = MarkovGenerador()
mgen.cargar(ruta_markov_generador)

print("\n----Se Inicia el Chat con", nombre + ".txt", "------")
print("-- Se aprenderá también el lenguaje del usuario --\n")
print(mgen.generar_texto())
terminar = False
while not terminar:
    try:
        entrada = user_input(ruta_log = ruta_log_user)
    except KeyboardInterrupt:
        terminar = True 
        print("\n----- FIN ------")
    else:
        ultima_palabra = entrada.split(' ')[-1]
        ultima_categoria = pos_tag([ultima_palabra])[0][1]
        siguiente_categoria = mgram.obtener_siguiente_categoria(ultima_categoria)
        siguiente_palabra = diccionario.escoger_palabra_de_categoria(siguiente_categoria)
        print(mgen.generar_texto(siguiente_palabra))
        mgen.reentrenar_con_cadena(entrada)
