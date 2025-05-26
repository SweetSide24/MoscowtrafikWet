from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit
import sqlite3
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
socketio = SocketIO(app)

@app.before_request
def before_request():
    if not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)

# Конфигурация базы данных
DATABASE = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Маршруты
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                          (username, password)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                        (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Username already exists"
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Пример данных о пробках (можно заменить на реальный API)
    traffic_data = [
        {"road": "Ленинский проспект", "level": "high", "speed": 20},
        {"road": "Кутузовский проспект", "level": "medium", "speed": 40},
        {"road": "Третье транспортное кольцо", "level": "high", "speed": 15},
        {"road": "Садовое кольцо", "level": "medium", "speed": 35},
        {"road": "Проспект Мира", "level": "low", "speed": 50}
    ]
    
    # Пример данных о погоде (можно заменить на реальный API)
    weather_data = {
        "temp": 15,
        "condition": "Облачно",
        "humidity": 75,
        "wind": 5
    }
    
    return render_template('dashboard.html', 
                         username=session['username'],
                         traffic_data=traffic_data,
                         weather_data=weather_data)
@app.route('/transport')
def transport():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('transport.html', username=session['username'])
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# WebSocket для чата
@socketio.on('message')
def handle_message(data):
    emit('message', {
        'username': session.get('username', 'Anonymous'),
        'message': data['message'],
        'time': datetime.now().strftime('%H:%M')
    }, broadcast=True)

if __name__ == '__main__':
    init_db()
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        ssl_context=('cert.pem', 'key.pem'),  # Убедитесь, что файлы лежат в той же папке
        debug=True,
        allow_unsafe_werkzeug=True  # Для обхода ошибки Werkzeug
    )