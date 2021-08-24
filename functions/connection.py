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
            print(name)
            name = name.encode('utf-8')
            
            
            
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
            
            database_title(records)   

        get_cast(link, id) 

        get_aka(link, id)

        get_relase(link, id)
        

def get_aka(link, id_title):


    scrap = page('https://www.themoviedb.org/'+link+'/titles')


    titles=scrap.find_all('table', 'card releases titles')

  
    for card in titles:

        
        country=card.find('h2','release')

        

        if country==None:
            pass

        else:
            country=country.get_text(strip=True)


        aka=card.tbody

        if aka==None:
            pass
        
        else:
            aka=aka.get_text(strip=True)


        records=[[country,aka,id_title]]

        
        database_aka(records)


def get_cast(link, id_title):

    
    scrap = page('https://www.themoviedb.org/'+link+'/cast')


    caster=scrap.find_all('ol', 'people credits')
    

    for cast in caster:
        persons=cast.find_all('p')

        for person in persons:

            name=person.find('a')

            if name==None:
                pass

            else:
                
                person_id=name.attrs['href']

                person_id=person_id.split('/')
                person_id=person_id[2]
                person_id=person_id.split('-')
                person_id=int(person_id[0])


                name=name.get_text(strip=True)

                character=person.find('p','character')

                if character==None:
                    pass
                else:
                    character=character.get_text(strip=True)


            if name!=None:

                records=[[person_id,name,character,id_title]]

                database_cast(records)   
    

def get_relase(link, id_title):

    scrap = page('https://www.themoviedb.org/'+link+'/releases')

    titles=scrap.find_all('table', 'card releases')


    for card in titles:

        country=card.find('h2','release')

        
        if country==None:
            pass

        else:
            country=country.get_text(strip=True)

        print( country)

        date=card.tbody.td.get_text(strip=True)

        print(date)

        records=[[country,date,id_title]]

        database_relases(records)


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
    

def database_title (records):
    

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


def database_cast (records):
    

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
    INSERT INTO cast_and_crew
    VALUES (?,?,?,?)
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


def database_aka(records):

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
    INSERT INTO aka
    VALUES (?,?,?)
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


def database_relases(records):

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
    INSERT INTO relases
    VALUES (?,?,?)
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
