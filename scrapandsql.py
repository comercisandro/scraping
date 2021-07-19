from os import name
from typing import overload
from functions.connection import page
from functions.connection import database






tmdb_query = tmdb_query = 'https://www.themoviedb.org/search?query='

tmdb = page(tmdb_query+'luca')


resultados = tmdb.find_all('a', 'result')
#print(resultados)
#print()
detectadas = 0
no_detectadas = 0
#records=[]

links = []

for resultado in resultados:
    
    if resultado['data-media-type']== 'movie':
        
        link = resultado.attrs['href']
        #print(link)
        #print()
        if link in links:
            pass
        else:
            links.append(link)

print(len(links))
print()

for link in links:
    scrap = page('https://www.themoviedb.org/'+link)

    encabezados = scrap.find_all('section', 'images inner')

    for encabezado in encabezados:
        name = encabezado.find('h2').a.text
        
        
        release=encabezado.find('span', 'release')
        
        if release==None:
            pass
        else:
            release=release.text.strip()
            #release=realase.get_text(strip=True)
            
            
            
        genres=encabezado.find('span','genres')
        
        if genres==None:
            pass
        else:
            genres=genres.get_text(strip=True)
        
        
        
        runtime=encabezado.find('span','runtime')
        
        if runtime==None:
            pass
        else:
            runtime=runtime.text.strip()
           
           
            
        user_score=encabezado.find('div','user_score_chart')['data-percent']
        
        if user_score==None:
            pass
        
        
        
        overview=encabezado.find('div', 'overview')
        
        if overview==None:
            pass
        else:
            overview=overview.get_text(strip=True)
        
        overview=overview.encode('utf-8')
        
        
        
        records=[[name,release,genres,runtime,user_score,overview]]
        print(records)
        database(records)


