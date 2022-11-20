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
        create table users(
            id serial not null, 
            firstname varchar(50), 
            lastname varchar(50),
            username varchar(30) not null,
            password varchar(64),
            primary key (id)
        )
    """ 
    
    cursor.execute(sql_create_table_users)

    sql_create_table_posts = """
        create table posts(
            id serial not null,
            user_id integer,
            title varchar(100),
            text varchar(500),
            primary key (id),
            foreign key (user_id) references users (id)
        )
    """

    cursor.execute(sql_create_table_posts)
except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)

finally:
    if conn:
        cursor.close()
    
    conn.close()
    print("Соединение с PostgreSQL закрыто")