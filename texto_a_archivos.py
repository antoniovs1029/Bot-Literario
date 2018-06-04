"""
Toma un archivo de texto en "./textos/archivo.txt" y genera los archivos necesarios que se podrán
usar en otros scripts para usar los bots.
"""

from modulos.gramatical import generar_archivos_ct_y_dic, MarkovGramatical, DiccionarioGramatical
from modulos.generacion import MarkovGenerador
from modulos.otros import crear_dir
import os
import sys

if len(sys.argv) == 2:
    # debe existir el archivo ./textos/nombre.txt
    nombre = sys.argv[1]
else:
    print("Error: Es necesario pasar el nombre del archivo a utilizar")
    exit()

ruta_texto = os.path.join(".", "textos", nombre + ".txt")

dir_generados = os.path.join(".", "generados")
crear_dir(dir_generados)
ruta_categtxt = os.path.join(dir_generados, nombre + ".categ.txt") 
ruta_dic = os.path.join(dir_generados, nombre + ".dic.pickle")
ruta_markov_gramatical = os.path.join(dir_generados, nombre + ".markov-gramatical.pickle")
ruta_markov_generador = os.path.join(dir_generados, nombre + ".markov-generador.pickle")


generar_archivos_ct_y_dic(ruta_texto, ruta_categtxt, ruta_dic, forzar = True)
diccionario = DiccionarioGramatical()
diccionario.cargar(ruta_dic)

mgram = MarkovGramatical()
mgram.entrenar(ruta_categtxt)
mgram.guardar(ruta_markov_gramatical)


mgen = MarkovGenerador()
mgen.entrenar(ruta_texto)
mgen.guardar(ruta_markov_generador)
