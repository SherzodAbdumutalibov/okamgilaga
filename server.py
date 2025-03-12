from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        routes = {
            "/": ("index.html", "text/html"),
            "/ping": ("pong", "text/plain"),
            "/hello": ("Привет, Пацаны!", "text/plain")
        }

        content, content_type = routes.get(self.path, ("404 Страница не найдена", "text/plain"))
        
        # Нужен для проверки index.html. Предупредит, если его нет в папке
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

def run(port=8000):
    server = HTTPServer(("", port), SimpleHandler)
    print(f"Сервер запущен на http://localhost:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run()
