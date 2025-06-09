import sqlite3

DB_NAME = "veritabanı.db"

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Kullanıcılar tablosu: Admin, Personel, Kullanıcı
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT NOT NULL,  -- admin, personel, kullanıcı
        password TEXT NOT NULL,
        added_by INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    transaction_type TEXT NOT NULL,  -- 'kiralama' veya 'satin_alma'
    transaction_date TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(book_id) REFERENCES books(id)
    )

    ''')

    # Kitaplar tablosu
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        category TEXT NOT NULL
    )
    ''')


    conn.commit()
    conn.close()

def add_user(name, role, password, added_by=None):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO users (name, role, password, added_by)
    VALUES (?, ?, ?, ?)
    ''', (name, role, password, added_by))

    conn.commit()
    conn.close()

def get_user(name, password):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT * FROM users WHERE name = ? AND password = ?
    ''', (name, password))
    user = cursor.fetchone()

    conn.close()
    return user

def add_book(name, price, category):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO books (name, price, category)
    VALUES (?, ?, ?)
    ''', (name, price, category))

    conn.commit()
    conn.close()

def list_books():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()

    conn.close()
    return books
def list_books_with_status():
    conn = connect_db()
    cursor = conn.cursor()

    query = '''
    SELECT b.id, b.name, b.price, b.category,
    (SELECT transaction_type FROM transactions t WHERE t.book_id = b.id ORDER BY transaction_date DESC LIMIT 1) as status
    FROM books b
    '''
    cursor.execute(query)
    books = cursor.fetchall()
    conn.close()
    return books

def add_transaction(user_id, book_id, transaction_type):
    conn = connect_db()
    cursor = conn.cursor()
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO transactions (user_id, book_id, transaction_type, transaction_date)
        VALUES (?, ?, ?, ?)
    ''', (user_id, book_id, transaction_type, now))
    conn.commit()
    conn.close()

def is_book_available(book_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT transaction_type FROM transactions
        WHERE book_id = ?
        ORDER BY transaction_date DESC LIMIT 1
    ''', (book_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return True
    if row[0] == "satin_alma":
        return False
    if row[0] == "kiralama":
        return False
