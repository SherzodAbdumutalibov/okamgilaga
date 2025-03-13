import sqlite3, json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import os

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        parsed_path = urlparse(self.path).path

        if parsed_path == "/":
            self.serve_html("index.html")
            return

        routes = {
            "/tables": lambda: [row[0] for row in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")],
            "/table_data": lambda: {t: cursor.execute(f"SELECT * FROM {t}").fetchall() for t in self.get_tables(cursor)}
        }

        data = routes.get(parsed_path, lambda: {"error": "Страница не найдена"})()
        conn.close()
        self.respond(200 if parsed_path in routes else 404, data)

    def serve_html(self, filename):
        if os.path.exists(filename):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            with open(filename, "rb") as file:
                self.wfile.write(file.read())
        else:
            self.respond(404, {"error": "Файл не найден"})

    def do_POST(self):
        if self.path != "/register":
            return self.respond(404, {"error": "Страница не найдена"})

        data = json.loads(self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8"))
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        if data["role"] == "admin" and cursor.execute("SELECT 1 FROM requests WHERE role='admin'").fetchone():
            response = {"status": "error", "message": "Админ уже существует"}
        else:
            cursor.execute("INSERT INTO requests (login, password, role) VALUES (?, ?, ?)", 
                           (data["login"], data["password"], data["role"]))
            conn.commit()
            response = {"status": "ok", "message": "Пользователь добавлен"}

        conn.close()
        self.respond(200, response)

    def get_tables(self, cursor):
        return [row[0] for row in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")]

    def respond(self, code, data):
        self.send_response(code)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")  # Разрешаем запросы с любого источника
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

HTTPServer(("localhost", 8000), SimpleHandler).serve_forever()
