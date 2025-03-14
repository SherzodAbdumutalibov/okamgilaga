import sqlite3


def listOfTables()
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    for col in columns:
        print(col)
    conn.close()



# Создаем таблицу, если её нет
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     username TEXT UNIQUE NOT NULL,
#     password TEXT NOT NULL
# )
# """)

# conn.commit()
# conn.close()
# print("Таблица users создана!")


# cursor.execute("SELECT * FROM users")
# users = cursor.fetchall()

# for user in users:
#     print(user)
# conn.close()

