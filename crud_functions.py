import sqlite3

def initiate_db():
    connect = sqlite3.connect('products.db')
    cursor = connect.cursor()
    try:
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS Products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    price INTEGER NOT NULL
                )
            """)
        connect.commit()
        print("Таблица Products успешно создана или уже существует.")
    except sqlite3.Error as e:
        print(f"Ошибка при создании таблицы: {e}")
    finally:
        connect.close()

    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    try:
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    balance INTEGER NOT NULL
                )
            """)
        connect.commit()
        print("Таблица Users успешно создана или уже существует.")
    except sqlite3.Error as e:
        print(f"Ошибка при создании таблицы: {e}")
    finally:
        connect.close()


initiate_db()

def add_user(username, email, age):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    try:
        cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)", (username, email, age, 1000))
        connect.commit()
        return True
    except sqlite3.IntegrityError:
        connect.rollback()
        return False
    except sqlite3.Error as e:
        connect.rollback()
        print(f"Ошибка при добавлении пользователя: {e}")
        return False
    finally:
        connect.close()

def is_included(username):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    try:
        cursor.execute("SELECT 1 FROM Users WHERE username = ?", (username,))
        result = cursor.fetchone()
        return result is not None
    except sqlite3.Error as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return False
    finally:
        connect.close()


def insert_products():
    connect = sqlite3.connect('products.db')
    cursor = connect.cursor()
    for i in range(1, 5):
        cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                           (f"Продукт {i}", f"Описание {i}", i*100))
    connect.commit()
    connect.close()

#insert_products()


def get_all_products():
    connect = sqlite3.connect('products.db')
    cursor = connect.cursor()
    try:
        cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()
        return products
    except sqlite3.Error as e:
        print(f"Ошибка при получении данных: {e}")
        return None
    finally:
        connect.close()