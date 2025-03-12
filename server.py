from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        routes = {
            "/": ("index.html", "text/html"),
            "/ping": ("pong", "text/plain"),
            "/hello": ("Привет, Пацаны!", "text/plain"),
            "/data": (json.dumps({"name": "Alice", "age": 25, "city": "Tashkent"}), "application/json")
        }

        content, content_type = routes.get(self.path, ("404 Страница не найдена", "text/plain"))

        # Проверка index.html
        if self.path == "/" and content == "index.html":
            try:
                with open(content, "r", encoding="utf-8") as f:
                    content = f.read()
            except FileNotFoundError:
                content, content_type = "Файл index.html не найден", "text/plain"

        self.send_response(200 if self.path in routes else 404)
        self.send_header("Content-type", f"{content_type}; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode())

        print(f"Запрос: {self.path} → Ответ: {content[:50]}...")

    def do_POST(self):
        if self.path == "/echo":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode("utf-8")

            try:
                data = json.loads(post_data)  # Загружаем JSON
                response = {"status": "ok", "received": data}
            except json.JSONDecodeError:
                response = {"status": "error", "message": "Invalid JSON"}

            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode())

            print(f"POST запрос: {post_data} → Ответ: {response}")

def run(port=8000):
    server = HTTPServer(("", port), SimpleHandler)
    print(f"Сервер запущен на http://localhost:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run()
