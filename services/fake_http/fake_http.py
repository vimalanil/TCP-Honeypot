import os
import sys
import datetime
from http.server import SimpleHTTPRequestHandler, HTTPServer

# Add project root to sys.path for module imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)

from utils.logger import log_event

# Path to serve fake website files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "site")

class FakeWebHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress default console log
        pass

    def log_http_access(self, method, url, user_agent, data=None):
        client_ip = self.client_address[0]
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_msg = f"[FAKE_SITE] {timestamp} | IP: {client_ip} | Method: {method} | URL: {url} | UA: {user_agent}"
        if data:
            log_msg += f" | Data: {data}"
        log_event(log_msg)

    def do_GET(self):
        user_agent = self.headers.get('User-Agent', 'Unknown')
        self.log_http_access("GET", self.path, user_agent)
        super().do_GET()

    def do_POST(self):
        user_agent = self.headers.get('User-Agent', 'Unknown')
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode(errors='ignore')
        self.log_http_access("POST", self.path, user_agent, post_data)

        # Send a fake response
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<h1>Thank you for submitting!</h1>")

def start_fake_http(host='0.0.0.0', port=8080):
    os.chdir(WEB_DIR)
    log_event(f"[HTTP] Fake website serving on http://{host}:{port}")
    httpd = HTTPServer((host, port), FakeWebHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    start_fake_http()

