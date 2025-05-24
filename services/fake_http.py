from http.server import BaseHTTPRequestHandler, HTTPServer
from utils.logger import log_event

class FakeHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        log_event(f"[HTTP] GET request from {self.client_address[0]} for path: {self.path}")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Fake HTTP Service</h1></body></html>")

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode(errors='ignore')
        log_event(f"[HTTP] POST request from {self.client_address[0]} to {self.path} with data: {post_data}")
        self.send_response(200)
        self.end_headers()

def start_fake_http(host='0.0.0.0', port=8080):
    server = HTTPServer((host, port), FakeHTTPRequestHandler)
    server.serve_forever()
