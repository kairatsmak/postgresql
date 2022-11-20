import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn = None

try:
    conn = psycopg2.connect(
        user = "postgres",
        password = "12345",
        host = "localhost",
        port = "5432",
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    conn.autocommit = True

    cursor = conn.cursor()

    sql_create_database = "create database postgres_db"
    
    cursor.execute(sql_create_database)
    
    # Распечатать сведения о PostgreSQL
    print("Информация о сервере PostgreSQL")
    print(conn.get_dsn_parameters(), "\n")
    # Выполнение SQL-запроса
    cursor.execute("SELECT version();")
    # Получить результат
    record = cursor.fetchone()
    print("Вы подключены к - ", record, "\n")

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)

finally:
    if conn:
        cursor.close()
    
    conn.close()
    print("Соединение с PostgreSQL закрыто")