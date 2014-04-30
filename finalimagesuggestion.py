# -*- coding: cp1252 -*-
import urllib2
import webbrowser
import math
import json
from pprint import *
import nltk 
import re
import flickrapi

url = []
global test

class F1:
    api_key = 'c96d6a956c000f6b0de1192f82a4b66c'
    api_secret = '74cc45607b849f11'
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format= 'json')
    (token, frob) = flickr.get_token_part_one(perms='write')
    if not token: raw_input("Press ENTER after you authorized this program")
    flickr.get_token_part_two((token, frob))
    def Search(self, arr, b):
        for i in range(len(arr)):
            flickresp = F1.flickr.photos_search(api_key = F1.api_key, tags= arr[i][0],text = arr[i][0], license = '6,4', per_page = b[i], nojsoncallback=1, sort= 'relevance')
            flickrdecoded = json.loads(flickresp)
            z=0
            for photo in flickrdecoded['photos']['photo']:
                id = flickrdecoded['photos']['photo'][z]['id']
                owner = flickrdecoded['photos']['photo'][z]['owner']
                url1 = "http://www.flickr.com/photos/"+ owner + '/' + id +'/'
                url.append(url1)
                z= z+1
    def Searchkeyw(self, keyw):
        flickresp = F1.flickr.photos_search(api_key = F1.api_key, tags= keyw,text = keyw, license = '6,4', per_page = '5', nojsoncallback=1, sort= 'relevance')
        flickrdecoded = json.loads(flickresp)
        z=0
        for photo in flickrdecoded['photos']['photo']:
            id = flickrdecoded['photos']['photo'][z]['id']
            owner = flickrdecoded['photos']['photo'][z]['owner']
            url1 = "http://www.flickr.com/photos/"+ owner + '/' + id +'/'
            url.append(url1)
            z= z+1
        
class NLTK:
    
    def entities(self, sentence):
        text = nltk.word_tokenize(sentence)
        tagged=nltk.pos_tag(text)
        namedentities = nltk.chunk.ne_chunk(tagged,binary=True)
        entities=re.findall(r'NE\s(.*?)/',str(namedentities))
        arr= []
        arr1 =set(entities)
        for i in arr1:
            t = entities.count(i)
            arr.append([i,t])
        print arr
        w = 0
        b = []
        for i in range(len(arr)):
            w= w + arr[i][1]    
        for i in range(len(arr)):
            temp = arr[i][1]*5/w
            if temp>1:
                b.append(int(math.floor(temp)))
            else:   
                b.append(1)
        print b
        w = wikim()
        w.Search(arr,b)
        f = F1()
        f.Search(arr,b)
        json_string = json.dumps(url)
        del url[:]
        test = json.loads(json_string)
        return test
    
class wikim:
    def Search(self,arr,b):
        for i in range(len(arr)):
            e = "http://commons.wikimedia.org/w/api.php?action=query&list=allimages&aiprop=url%7Cmime&format=json&redirects&aifrom="+arr[i][0] + "&ailimit=" + str(b[i])
            req = urllib2.Request(e)
            f = urllib2.urlopen(req)
            response = f.read()
            f.close()
            r= json.loads(response)
            for z in range(b[i]):
                a = r['query']['allimages'][z]['url']
                url2 = a
                url.append(url2)
    def Searchkeyw(self, keyw):
        e = "http://commons.wikimedia.org/w/api.php?action=query&list=allimages&aiprop=url%7Cmime&format=json&redirects&aifrom="+keyw + "&ailimit=" + str(5)
        req = urllib2.Request(e)
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
        r= json.loads(response)
        for z in range(5):
            a = r['query']['allimages'][z]['url']
            url2 = a
            url.append(url2)
  
def Searchkeyw(keyw):
    w = wikim()
    w.Searchkeyw(keyw)
    f = F1()
    f.Searchkeyw(keyw)
    json_string = json.dumps(url)
    del url[:]
    test = json.loads(json_string)
    return test
 
