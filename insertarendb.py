import sys
import pypyodbc as odbc

records = [
    ['michus quest','2020','adventure','1 year','9.8','la vida del michu','gato rompe bola']
]

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
    VALUES (?,?,?,?,?,?,?)
"""

try:
    for record in records:
        print(record)
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
    