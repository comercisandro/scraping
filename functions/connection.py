#from _typeshed import NoneType
import requests
from bs4 import BeautifulSoup
import sys
import pypyodbc as odbc

def page (url):


    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })


    page= requests.get(url, headers=headers)
    soup=BeautifulSoup(page.content, 'html.parser')
    #soup=BeautifulSoup(page.text, 'lxml')
    
    #print(soup.head.title)
    
    return(soup)

def pages_num(tmdb):
    
    max_page=0
    paginas = tmdb.find_all('div', 'pagination')
    for pagina in paginas:
        
        if pagina['custom_path_info']== '/search/movie':
            numeros_pag=pagina.find_all('a')
            max_page=numeros_pag[-2].get_text()
     
    print('Cantidad de paginas:', max_page)
    max_page=int(max_page)            
    return max_page
        

def movie_links(tmdb):
    
    resultados = tmdb.find_all('a', 'result')
    
    links=[]
    
    for resultado in resultados:

        if resultado['data-media-type']== 'movie':
            
            link = resultado.attrs['href']
            if link in links:
                pass
            else:
                links.append(link) 
                
    return links   

def get_titles(links):
    
    for link in links:
        scrap = page('https://www.themoviedb.org/'+link)

        id=link.split('/')
        id=id[2]

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
            
            
            
            records=[[id,name,release,genres,runtime,user_score,overview]]
            #print(records)
            
            
            database(records)    

         
def next_page(tmdb):
    paginas = tmdb.find_all('div', 'pagination')
    
    for pagina in paginas:
        if pagina['custom_path_info']== '/search/movie':
            proxima=pagina.find('a','next_page')
            if proxima!=None:
                proxima=proxima.attrs['href']
                tmdb_query = 'https://www.themoviedb.org'+proxima
                print(tmdb_query)
                return tmdb_query
            else:
                pass
    


def database (records):
    

    DRIVER = 'ODBC Driver 17 for SQL Server'
    SERVER_NAME = 'localhost'
    DATABASE_NAME = 'tmdb'

    conn_string = f"""
        Driver={{{DRIVER}}};
        Server={SERVER_NAME};
        Database={DATABASE_NAME};
        Trust_Connection=yes;
        UID=sa;
        PWD=Sql79803233;
    """

    try:
        conn= odbc.connect(conn_string)
        print(conn)
        
    except Exception as e:
        print(e)
        print('task is terminated')
        sys.exit
        
    else:
        cursor= conn.cursor()
        
    
    insert_statement="""
    INSERT INTO title
    VALUES (?,?,?,?,?,?,?)
    """ 
    
        
        
    try:
        for record in records:
            #print(record)
            cursor.execute(insert_statement, record)
        
    except Exception as e:
        cursor.rollback()
        print(e.value)
        print('transaction rolled back')
        
    else:
        print('records inserted successfully')
        cursor.commit()
        cursor.close()
        
    finally:
        if conn.connected==1:
            print('connection closed')
            conn.close()    
