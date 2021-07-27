
from functions.connection import movie_links, next_page, page, pages_num, movie_links, get_titles,next_page



tmdb_query = 'https://www.themoviedb.org/search?query='+'luca'

tmdb = page(tmdb_query)




# BUSCANDO LA CANTIDAD DE PAGINAS


max_page=pages_num(tmdb)


for pagnum in range(max_page):
    
    tmdb = page(tmdb_query)
    
    links=movie_links(tmdb)
    
    get_titles(links)
    
    tmdb_query=next_page(tmdb)
    
   
 

