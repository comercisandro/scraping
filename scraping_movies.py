import requests
import time
import csv
import re
from bs4 import BeautifulSoup

import pandas as pd


def page (url):

#url='https://www.imdb.com/'

    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })


    page= requests.get(url, headers=headers)
    soup=BeautifulSoup(page.content, 'html.parser')
    #soup=BeautifulSoup(page.text, 'lxml')
    
    #print(soup.head.title)
    
    return(soup)

detectadas=0
no_detectadas=0

tmdb_query='https://www.themoviedb.org/search?query='

peliculas = "Peliculas.txt"
with open(peliculas, "r") as archivo:
    
    
    
    
    for linea in archivo:
        pelicula=linea.replace(' ','+')
    
        print(pelicula)
        
        tmdb=page(tmdb_query+linea)
        
        titulos=tmdb.find_all('a', 'result')
        
        
        
        if not titulos:
            print('Pelicula no detectada')
            no_detectadas+=1
        
        else:
            
            detectadas+=1
            for titulo in titulos:
                link=titulo.attrs['href']
                print(link)
    
            
print('Peliculas detectadas:',detectadas)
print('Peliculas no detectadas:',no_detectadas)

