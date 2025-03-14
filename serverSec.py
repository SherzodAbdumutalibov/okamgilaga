import sqlite3, json
from http.server import BaseHTTPRequestHandler, HTTPServer

class SecureHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")

        try:
            data = json.loads(post_data)
            login, password = data.get("login"), data.get("password")

            if not login or not password:
                raise ValueError("Поля login и password обязательны")

        except (json.JSONDecodeError, ValueError) as e:
            return self.respond(400, {"status": "error", "message": str(e)})

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # ✅ Защита: Используем параметризованный SQL-запрос
        cursor.execute("SELECT * FROM requests WHERE login=? AND password=?", (login, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.respond(200, {"status": "ok", "role": user[3]})
        else:
            self.respond(403, {"status": "error", "message": "Неверные данные"})

    def respond(self, code, data):
        self.send_response(code)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

HTTPServer(("localhost", 8000), SecureHandler).serve_forever()
