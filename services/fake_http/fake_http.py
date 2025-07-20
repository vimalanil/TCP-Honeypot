import os
import sys
from http.server import SimpleHTTPRequestHandler, HTTPServer

# Add project root to sys.path for module imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)

from utils.logger import log_event

# Path to serve fake website files (HTML, JS, CSS)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "site")  # You can place fake login pages etc. here

class FakeWebHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Log basic requests
        log_event(f"[HTTP] {self.client_address[0]} - {format % args}")

    def do_GET(self):
        # Log GET request
        log_event(f"[HTTP] GET {self.path} from {self.client_address[0]}")
        super().do_GET()

    def do_POST(self):
        # Handle and log POST request data
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode(errors='ignore')
        log_event(f"[HTTP] POST {self.path} from {self.client_address[0]} with data: {post_data}")
        
        # Respond to the POST
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<h1>Thank you for submitting!</h1>")

def start_fake_http(host='0.0.0.0', port=8080):
    # Change to fake website directory before serving
    os.chdir(WEB_DIR)
    httpd = HTTPServer((host, port), FakeWebHandler)
    log_event(f"[HTTP] Fake website serving on http://{host}:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    start_fake_http()

