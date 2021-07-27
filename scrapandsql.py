from os import name
from typing import overload
from functions.connection import page
from functions.connection import database


tmdb_query = 'https://www.themoviedb.org/search?query='+'luca'

tmdb = page(tmdb_query)

#links = []

resultados = tmdb.find_all('a', 'result')


# BUSCANDO LA CANTIDAD DE PAGINAS
paginas = tmdb.find_all('div', 'pagination')

contador_solo_movies=0
for pagina in paginas:
    
    if contador_solo_movies==0:
        next=pagina.get_text()
        next=next.split('Next')
        max_page=int(next[0][-2])
        print(max_page)
        contador_solo_movies+=1


        
        
        
               
   
for pagnum in range(max_page):
    
    links=[]
    
    tmdb = page(tmdb_query)
    
    resultados = tmdb.find_all('a', 'result')
    
    
    for resultado in resultados:

        if resultado['data-media-type']== 'movie':
            #print(resultado)
            link = resultado.attrs['href']
            #print(link)
            #print()
            if link in links:
                pass
            else:
                links.append(link)
    #print(links)
    
    
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
            #print(records)
            
            
            database(records)
    
    
    paginas = tmdb.find_all('div', 'pagination')
    movies=0
    for pagina in paginas:
        
        
        
        if movies==0 and max_page>1:
            proxima=pagina.find('a','next_page')
            proxima=proxima.attrs['href']
            tmdb_query = 'https://www.themoviedb.org'+proxima

            movies+=1
            
            print(max_page)
            max_page-=1
            
        else:
            pass
            
    print(tmdb_query)
        
    #proxima=pagina.find_all('a','next_page')
    #proxima=proxima.attrs['href']
    #print (tmdb)
    #

            


'''


for pagina in paginas:
    pagina_text=pagina
    print(pagina_text.prettify())
    




for pagina in paginas:
    nexts=pagina.find_all('a', 'next_page')
    for next in nexts:
        proximo=next.attrs['href']
        proximo_movie=proximo.split('?')
        #if proximo_movie[0]=='/search/movie':
         #   print(proximo)
         
print(next)
         
         
         





for resultado in resultados:
    
    if resultado['data-media-type']== 'movie':
        print(resultado)
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
        '''
