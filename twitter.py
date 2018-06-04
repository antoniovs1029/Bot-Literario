import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import API
from twitter_keys import *

import os

from modulos.gramatical import generar_archivos_ct_y_dic, MarkovGramatical, DiccionarioGramatical
from modulos.generacion import MarkovGenerador
from modulos.otros import user_input_twitter, crear_dir
from nltk import pos_tag

nombre = 'rayuela'

print("Se cargara ./textos/" + nombre + ".txt")

dir_generados = os.path.join(".", "generados")
ruta_dic = os.path.join(dir_generados, nombre + ".dic.pickle")
ruta_markov_gramatical = os.path.join(dir_generados, nombre + ".markov-gramatical.pickle")
ruta_markov_generador = os.path.join(dir_generados, nombre + ".markov-generador.pickle")

dir_user_logs = os.path.join(".", "user_logs")
ruta_log_user = os.path.join(dir_user_logs, "twitter." + nombre + ".userlog.txt")


diccionario = DiccionarioGramatical()
diccionario.cargar(ruta_dic)

mgram = MarkovGramatical()
mgram.cargar(ruta_markov_gramatical)

mgen = MarkovGenerador()
mgen.cargar(ruta_markov_generador)


class listener(StreamListener):

    def on_data(self,data):
        data=json.loads(data)

        entrada = user_input_twitter(data['text'], ruta_log = ruta_log_user)
        ultima_palabra = entrada.split(' ')[-1]
        ultima_categoria = pos_tag([ultima_palabra])[0][1]
        siguiente_categoria = mgram.obtener_siguiente_categoria(ultima_categoria)
        siguiente_palabra = diccionario.escoger_palabra_de_categoria(siguiente_categoria)        
        respuesta = mgen.generar_texto(siguiente_palabra)

        try:
            print(data["id"], data["text"])
            api = API(auth)
            api.update_status(
                "@" + data["user"]["screen_name"] + " " + respuesta, in_reply_to_status_id=data["id"])


        except Exception as _:
            pass
        return True

    def on_error(self, status):
        print(status)


auth = OAuthHandler(ConsumerKey, ConsumerSecret)
auth.set_access_token(AccessToken, AccessTokenSecret)


#ment = API(auth)
#mentions = ment.mentions_timeline()
#mentions = json.loads(mentions)
#for m in mentions:
#print(mentions[0].text)
print("Se iniciara el stream")
twitterStream = Stream(auth, listener())
#twitterStream.filter(track=["@CEstocastico"])
twitterStream.filter(track=["@CortazarEstoc"])

