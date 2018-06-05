import json
import os
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import API
from twitter_keys import *

# para dormir al bot en caso de abusos...
from time import sleep

from modulos.gramatical import generar_archivos_ct_y_dic, MarkovGramatical, DiccionarioGramatical
from modulos.generacion import MarkovGenerador
from modulos.otros import user_input_twitter, crear_dir
from nltk import pos_tag

nombre = 'rayuela'

print("Se cargara ./textos/" + nombre + ".txt")

dir_generados = os.path.join(".", "generados")
ruta_dic = os.path.join(dir_generados, nombre + ".dic.pickle")
ruta_markov_gramatical = os.path.join(
    dir_generados, nombre + ".markov-gramatical.pickle")
ruta_markov_generador = os.path.join(
    dir_generados, nombre + ".markov-generador.pickle")

dir_user_logs = os.path.join(".", "user_logs")
ruta_log_user = os.path.join(
    dir_user_logs, "twitter." + nombre + ".userlog.txt")


diccionario = DiccionarioGramatical()
diccionario.cargar(ruta_dic)

mgram = MarkovGramatical()
mgram.cargar(ruta_markov_gramatical)

mgen = MarkovGenerador()
mgen.cargar(ruta_markov_generador)


class listener(StreamListener):

    def on_data(self, data):
        data = json.loads(data)
        # crea directorio logs si no existe, faltaba llamar la función.
        crear_dir(dir_user_logs)
        entrada = user_input_twitter(data['text'], ruta_log=ruta_log_user)
        ultima_palabra = entrada.split(' ')[-1]
        ultima_categoria = pos_tag([ultima_palabra])[0][1]
        siguiente_categoria = mgram.obtener_siguiente_categoria(
            ultima_categoria)
        siguiente_palabra = diccionario.escoger_palabra_de_categoria(
            siguiente_categoria)
        respuesta = mgen.generar_texto(siguiente_palabra)

        try:
            print(data["user"]["screen_name"]+"'s tweet:", data["id"], data["text"])            
            api = API(auth)
            # mostrar en consola la respuest
            print("Respuesta Julio: "+respuesta)
            # no responder tweet instantáneamente, se ve muy de stalker
            sleep(5)
            api.update_status("@" + data["user"]["screen_name"] + " " + respuesta, in_reply_to_status_id=data["id"])

        except Exception as exc:
            print("ocurrió la excepción", exc)
        return True

    def on_error(self, status_code):
        # 30 minutos de espera en caso de un error
        secs = 1800
        if status_code == 420:
            # Se ha intentando iniciar sesión muchas veces en poco tiempo.
            print("Err: " + status_code + " - Enhance Your Calm!")
            print("Reconectando en", secs, "secs")
            sleep(secs)
        return True


auth = OAuthHandler(ConsumerKey, ConsumerSecret)
auth.set_access_token(AccessToken, AccessTokenSecret)
#ment = API(auth)
#mentions = ment.mentions_timeline()
#mentions = json.loads(mentions)
#for m in mentions:
#print(mentions[0].text)
print("Se iniciara el stream")
while True:
    # Para iniciar de nuevo el streaming en caso de algún error
    twitterStream = Stream(auth, listener())
    #twitterStream.filter(track=["@CEstocastico", "@cestocastico"])
    twitterStream.filter(track=["@CortazarEstoc", "cortazarestoc"])
