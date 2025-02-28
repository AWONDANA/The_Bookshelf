from flask import Flask, request, redirect, url_for, render_template
import mysql.connector

app = Flask(__name__)

db_config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'library_db'
}
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO books (title, author, year) VALUES (%s, %s, %s)', (title, author, year))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)
