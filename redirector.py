from http.server import BaseHTTPRequestHandler, HTTPServer

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', f'http://{self.server.server_address[0]}:8080')
        self.end_headers()

server_address = ('0.0.0.0', 80)
httpd = HTTPServer(server_address, RedirectHandler)
print("[+] Redirect server running on port 80 → 8080")
httpd.serve_forever()
