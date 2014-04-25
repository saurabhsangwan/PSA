# -*- coding: cp1252 -*-
import urllib2
import webbrowser
import math
import json
from pprint import *
import nltk 
import re
import wikitools
from wikitools import wiki
from wikitools import api
import flickrapi
api_key = 'c96d6a956c000f6b0de1192f82a4b66c'
api_secret = '74cc45607b849f11'
flickr = flickrapi.FlickrAPI(api_key, api_secret, format= 'json')
(token, frob) = flickr.get_token_part_one(perms='write')
if not token: raw_input("Press ENTER after you authorized this program")
flickr.get_token_part_two((token, frob))

sentence="""Sony tiene nuevo teléfono en su gama de entrada, se llama Sony Xperia E1, y curiosamente se ha decidido presentar fuera del CES, donde el Sony Xperia Z1 Compact iba a ser el protagonista. En el catálogo de los japoneses tenemos teléfonos de todos los tamaños, el nuevo llega para situarse en el primer escalón, con una pantalla de cuatro pulgadas.
Si ya nos habían sorprendido con un dispositivo de última tecnología en tamaño relativamente pequeño como el Compact, ahora han decidido que también es posible un terminal con especificaciones moderadas, pero buen aspecto externo.
El Sony Xperia E1 cuenta con un diseño similar al de su hermano más lujoso, y nos prometen que en la mano va a lucir muy parecido. Han aprovechado para enfocarlo más hacia el aspecto multimedia, con botones dedicados y un altavoz potente.
Esperamos las primeras tomas de contacto e imágenes reales para comprobar el tipo de materiales y construcción utilizados, por lo que vemos pinta bastante bien. Pasando a las especificaciones, son sencillas, como así nos prueba su corazón Qualcomm de cuatro núcleos, o la pantalla con resolución WVGA (800×480 píxeles). En la web oficial aseguran que es un MSM8210 de doble núcleo, si nos vamos a la web de Qualcomm, eso corresponde con un Snapdragon 200, que únicamente existe en configuración de cuatro núcleos.

Otras especificaciones que nos hablan de sus posibilidades reales son la justa memoria RAM – 512MB -, o los 4GB de memoria interna. Afortunadamente con KitKat, que es la versión Android con la que aparece en el mercado (está por confirmar), hay espacio para teléfonos menos capaces.
El otro aspecto llamativo del teléfono es el potente altavoz trasero, tanto que registra 100dB – un terror para algunos -. Sony lo acompaña de las tecnologías ClearAudio+ y xLoud para asegurar que el sonido además se propaga con calidad. No se me olvida, la batería es de 1.700mAh.
El teléfono presenta además un botón dedicado Walkman, con él podemos acceder directamente a la aplicación multimedia, y también reconocerá nuestros gestos -agitar el móvil – para ir cambiando de canción. Se regala un pase de 30 días al servicio de música Sony Entertainment Network2.
Walkman

Entre los detalles que no nos gustan tanto – había que recortar -, tenemos poca memoria interna, y la cámara es muy sencilla – 3 megapíxeles -, ya que no cuenta con enfoque automático ni está acompañada por flash. Tampoco hay cámara frontal.
Sony lo va a lanzar inicialmente en mercados emergentes – China, Oriente Medio, África y Asia-Pacífico – , por lo que nos lo veremos por aquí, o en Estados Unidos. Tampoco hay información concreta sobre precio o fechas de lanzamiento.
Para terminar de conocerlo, su conectividad se queda en 3G/HSPA+, contará con versión Dual SIM, y estará disponible en tres colores: blanco, negro y púrpura. Por cierto, ha sido presentado a la par que una nueva phablet, Sony Xperia T2 Ultra.
Actualización: el blog especializado XperiaBlog se atreve a dar precios para Europa. Nos cuentan que el Xperia E1 costará 129 euros en Bélgica, 139 euros en Alemania, y 149 euros en Holanda."""
text = nltk.word_tokenize(sentence)
tagged=nltk.pos_tag(text)
namedentities = nltk.chunk.ne_chunk(tagged,binary=True)
entities=re.findall(r'NE\s(.*?)/',str(namedentities))
arr= []
arr1 =set(entities)
for i in arr1:
    t = entities.count(i)
    arr.append([i,t])


url = []    
print arr
w = 0
b = []
for i in range(len(arr)):
    w= w + arr[i][1]    
for i in range(len(arr)):
    temp = arr[i][1]*10/w
    if temp>1:
        b.append(int(math.floor(temp)))
    else:   
        b.append(1)
print b

site = wiki.Wiki("http://commons.wikimedia.org/w/api.php")

for i in range(len(arr)):
    flickresp = flickr.photos_search(api_key = api_key, tags= arr[i][0],text = arr[i][0], license = '6,4', per_page = b[i], nojsoncallback=1, sort= 'relevance')
    flickrdecoded = json.loads(flickresp)
    #pprint(flickrdecoded)
    z=0
    for photo in flickrdecoded['photos']['photo']:
            id = flickrdecoded['photos']['photo'][z]['id']
            owner = flickrdecoded['photos']['photo'][z]['owner']
            url1 = "http://www.flickr.com/photos/"+ owner + '/' + id +'/'
            #print url1
            url.append(url1)
            #webbrowser.open(url,new=1)
            z= z+1
    d = arr[i][0]
    e = "http://commons.wikimedia.org/w/api.php?action=query&list=allimages&aiprop=url%7Cmime&format=json&redirects&aifrom="+ d + "&ailimit=" + str(b[i])
    req = urllib2.Request(e)
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
    r= json.loads(response)
    #pprint(r)
    for z in range(b[i]):
        a = r['query']['allimages'][z]['url']
        url2 = a
        #print url2
        url.append(url2)
        #webbrowser.open(url,new=1)
print url
json_string = json.dumps(url)
print json_string
test = json.loads(json_string)
pprint(test)
