import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON


###Credenciales de la cuenta de Twitter########################
#Poner aqui las credenciales de su cuenta privada, caso contrario la API bloqueara esta cuenta de ejemplo
ckey = "bOFL9PkXLt85j2k8QFwEjXgfd"
csecret = "VHvPjNbYFe9NmVDxq4YkRpBwuBvv1hIV7C16zF3mMWlgK10Bo4"
atoken = "872555876007247877-8fEo6PkqulZBsM5Olsb1jD7PXvBgXJQ"
asecret = "fQpUpmHWvX5ZAIK50ZOPB0r6LQ0aUBst9ZUSeNd7XtOI0"
#####################################

class listener(StreamListener):
    
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
            #Antes de guardar el documento puedes realizar parseo, limpieza y cierto analisis o filtrado de datos previo
            #a guardar en documento en la base de datos
            doc = db.save(dictTweet) #Aqui se guarda el tweet en la base de couchDB
            print ("Guardado " + "=> " + dictTweet["_id"]);
        except:
            print ("Documento ya existe");
            pass
        return True
    
    def on_error(self, status):
        print (status);
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

#Setear la URL del servidor de couchDB
server = couchdb.Server('http://localhost:5984/')
try:
    #Si no existe la Base de datos la crea
    db = server.create('final_confed2')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['final_confed2']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
twitterStream.filter(locations=[5.87,47.27,15.04,55.08])
twitterStream.filter(track=['ChilevsAlemania'])