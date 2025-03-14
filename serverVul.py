import sqlite3, json, os
from http.server import BaseHTTPRequestHandler, HTTPServer

conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
# cursor.execute("INSERT OR IGNORE INTO users VALUES ('admin', 'admin')")
conn.commit()
conn.close()

def listOfUsers():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        print(user)
    conn.close()

def listOfTables():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    for col in columns:
        print(col)
    conn.close()

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            if os.path.exists("index.html"):
                with open("index.html", "r", encoding="utf-8") as file:
                    self.wfile.write(file.read().encode("utf-8"))
            else:
                self.wfile.write("<h1>Ошибка: index.html не найден!</h1>".encode("utf-8"))
        else:
            self.respond(404, {"message": "Страница не найдена"})


    def do_POST(self):
        if self.path != "/login":
            self.respond(404, {"message": "Страница не найдена"})
            return
        
        content_length = int(self.headers["Content-Length"])
        data = eval(self.rfile.read(content_length).decode("utf-8"))
        
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (data["username"], data["password"]))
        user = cursor.fetchone()
        conn.close()

        if user:
            role = "админ" if user[1] == "admin" else "пользователь"
            self.respond(200, {"message": f"Вход выполнен! Вы {role}."})
        else:
            self.respond(403, {"message": "Неверные логин или пароль"})

    def respond(self, code, data):
        self.send_response(code)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))


print("Сервер запущен на http://localhost:8000")
HTTPServer(("localhost", 8000), SimpleHandler).serve_forever()
