import hashlib
import sqlite3

from flask import Flask, render_template, url_for, request, session, redirect, g

# конфигурация
DATABASE = '/tmp/main.db'
DEBUG = True
SECRET_KEY = ';lasu509483qhja;asdlf#()*&dlfsa;jf'

db = sqlite3.connect('users.db', check_same_thread=False)
cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    email Text NOT NULL,
    login Text NOT NULL,
    password TEXT NOT NULL
)""")
db.commit()
# надо чтобы работало xD
app = Flask(__name__)
app.config.from_object(__name__)
# app.config['SECRET_KEY'] = ';lasu509483qhja;asdlf#()*&dlfsa;jf' # этот ключ вроде уже не нужен тк есть другой


# это для подключения DATABASE


# дальше идут страницы (потом надо перенести в отдельный сайт для оптимизации кода)
menu = ['Главная страница', 'Админка', 'Создатели']

"""TODO: Переделать все под регистрацию"""
"""TODO: сделать кнопки: уже есть учетная запись или зарегистрироваться"""


@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'userLogged' in session:  # если чел зареган перекунуть его (пока что в рут)
        return redirect(url_for('root', login_id=session['userLogged']))


    elif request.method == 'POST':
        email_ = request.form['email']
        login_ = request.form['login_id']
        password_ = request.form['password']
        p_hash = hashlib.md5(password_.encode())
        password_hash_ = p_hash.hexdigest()
        cursor.execute(f"SELECT login FROM users WHERE login = '{login_}' ")
        if cursor.fetchone() is None:
            db.execute("INSERT INTO users VALUES (?,?,?)", (email_, login_, password_hash_))
            db.commit()
            session['userLogged'] = request.form['login_id']
            return redirect(url_for('root', login_id=session["userLogged"]))
            db.close()
        else:
            print("такой логин уже используетсья")

    return render_template('register.html', title='Register')


# это все к чертям переписать
@app.route('/login', methods=['POST', 'GET'])
def login():
    print(url_for('login'))
    print(request.form)


    if 'userLogged' in session:
        return redirect(url_for('root', login_id=session['userLogged']))

    elif request.method == 'POST':
        login_ = request.form['login_id']
        password_ = request.form['password']
        p_hash = hashlib.md5(password_.encode())
        password_hash_ = p_hash.hexdigest()

        cursor.execute(f"SELECT login AND password FROM users WHERE login = '{login_}' AND password = '{password_hash_}'")
        if cursor.fetchone():
            session['userLogged'] = request.form['login_id']
            return redirect(url_for('root', login_id=session["userLogged"]))
            db.close()
        else:
            return redirect(url_for('login'))
    return render_template('login.html', title='Login')


@app.route('/')
def index():
    print(url_for('index'))
    return render_template('main.html', title='Main', menu=menu)


# Добавить проверку на админа
@app.route('/root')
def root():
    print(url_for('root'))
    if 'userLogged' in session:
        pass
    else:
        return redirect(url_for('login'))

    return render_template('root.html', title='Admin Panel')


@app.route('/creators')
def creators():
    print(url_for('creators'))
    return render_template('creators.html', title='Creators')


@app.route('/profile/<username>/<path>')
def profile(username, path):
    return f'Пользователь: {username}, {path}'


@app.errorhandler(404)
def pageNotFound(error):
    return login()


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link.db'):
        g.link_db.close()


# это вот надо чтоб работало xD
if __name__ == '__main__':
    app.run(debug=True)
