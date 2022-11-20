import psycopg2
from psycopg2 import Error

def init_db() -> list:
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
        return conn, cursor, None
    except (Exception, Error) as error:
        return None, None, error

def check_user(cursor: object, username: str, password: str) -> bool:
    sql = "SELECT id, firstname, lastname FROM users WHERE username=%s and password=%s"
    cursor.execute(sql, (username, password))
    record = cursor.fetchone()
    return record

def get_posts(cursor: object):
    sql = """
        SELECT posts.id, posts.title, posts.text, users.firstname, users.lastname 
        FROM posts 
        INNER JOIN users ON posts.user_id = users.id 
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    posts = []
    for row in rows:
        post = {}
        post['id'] = row[0]
        post['title'] = row[1]
        post['text'] = row[2]
        post['user'] = {}
        post['user']['firstname'] = row[3]
        post['user']['lastname'] = row[4]
        posts.append(post)        
    return posts

def save_post(cursor: object, post: dict) -> None:
    if post['id']:
        sql = """
            UPDATE posts SET 
                title = %s,
                text = %s,
                user_id = %s
            WHERE
                id = %s
        """
        cursor.execute(sql, (post['title'], post['text'], post['user_id'], post['id']))
    else:
        sql = """
            INSERT INTO posts(title, text, user_id) 
            VALUES(%s, %s, %s)
        """
        cursor.execute(sql, (post['title'], post['text'], post['user_id']))


def get_post(cursor: object, post_id: int) -> dict:
    sql = "SELECT id, title, text FROM posts WHERE id=%s"
    cursor.execute(sql, (post_id,))
    record = cursor.fetchone()
    if record:
        post = {}
        post["id"] = record[0]
        post["title"] = record[1]
        post["text"] = record[2]
        return post
    else:
        return None    
# test
# conn, cursor, error = init_db()

# if error:
#     print("Ошибка при работе с PostgreSQL", error)
#     exit()

# sql = "SELECT * FROM users WHERE username='test_user' and password='12345'"
# cursor.execute(sql)
# record = cursor.fetchone()
# print(record)

