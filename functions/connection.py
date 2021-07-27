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


def database (records):
    

    DRIVER = 'ODBC Driver 17 for SQL Server'
    SERVER_NAME = 'sandro-X751LKB'
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
    VALUES (?,?,?,?,?,?)
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
