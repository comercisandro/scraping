import time
inicio = time.time()

from pypyodbc import NO_FREE_STATEMENT
from functions.connection import movie_links, next_page, page, pages_num, movie_links, get_titles, get_cast, next_page


no_encontrados=0
encontrados=0
titulos= "/home/sandro/Documentos/reportv/scraping/tmdb/peliculas.txt"

with open(titulos, "r") as titulos:

    for titulo in titulos:

        titulo=titulo.replace(' ','+')
        


        tmdb_query = 'https://www.themoviedb.org/search?query='+titulo
        
        


        tmdb = page(tmdb_query)
        


        # BUSCANDO LA CANTIDAD DE PAGINAS


        max_page=pages_num(tmdb)

        if max_page==0:
            print('titulo: ',titulo,' no encontrado' )
            no_encontrados+=1
            max_page=1

        elif max_page!=0:
            encontrados+=1
            print('titulo: ',titulo,' encontrado!' )

        for pagnum in range(max_page):
            
            tmdb = page(tmdb_query)
            
            links=movie_links(tmdb)

            #print(links)
            
            get_titles(links)
            
            tmdb_query=next_page(tmdb)
    
   
print('Titulos encontrados:',encontrados)
print('Titulos no encontrados:',no_encontrados)
fin = time.time()
print('Tiempo de ejecucion', (fin-inicio)/60 ) 
