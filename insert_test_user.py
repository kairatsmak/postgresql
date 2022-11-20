import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn = None

try:
    conn = psycopg2.connect(
        database = "postgres_db",
        user = "postgres",
        password = "12345",
        host = "localhost",
        port = "5432",
    )

    conn.autocommit = True

    cursor = conn.cursor()

    sql_create_table_users = """
       insert into users(firstname, lastname, username, password) values('Test', 'Test', 'test_user', '12345')
    """ 
    
    cursor.execute(sql_create_table_users)
except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)

finally:
    if conn:
        cursor.close()
    
    conn.close()
    print("Соединение с PostgreSQL закрыто")