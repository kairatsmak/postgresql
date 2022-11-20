from flask import Flask, request, render_template, redirect

from service import *

app = Flask(__name__)

is_logged = False
current_user = None

conn, cursor, error = init_db()

if error:
    print("Ошибка при работе с PostgreSQL", error)
    exit()

# Main page
@app.route("/")
def index():
    global is_logged, current_user

    if is_logged == False:
        return redirect("http://localhost:8000/login")

    posts = get_posts(cursor)
    return render_template('index.html', posts=posts, user=current_user)

# Login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    global is_logged, current_user

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        record = check_user(cursor, username, password)
        if record:
            is_logged = True
            current_user = {
                'id': record[0],
                'firstname': record[1],
                'lastname': record[2],
            }
            return redirect("http://localhost:8000/")
        else:
            error_msg = "Имя пользователя или пароль не верны!"
            return render_template('login.html', username=username, error_msg=error_msg)
    
    else:
        return render_template('login.html')

# Post page
@app.route("/post", methods=['GET', 'POST'])
def post():
    global is_logged, current_user

    if is_logged == False:
        return redirect("http://localhost:8000/login")

    if request.method == 'POST':
        post = {}
        post['id'] = request.form['id']
        post['title'] = request.form['title']
        post['text'] = request.form['text']
        post['user_id'] = current_user["id"]
        save_post(cursor, post)
        return redirect("http://localhost:8000/")
    else:
        post_id = request.args.get('post_id')
        post = None
        if post_id:
            post = get_post(cursor, post_id)
        return render_template('post.html', post=post)

if __name__ == "__main__":
    app.run(host='localhost', port=8000, debug=True)