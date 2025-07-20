import socket
import threading
import logging
import os
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from utils.geoip_lookup import get_geoip_info
from services.fake_ssh.ssh_server import handle_ssh
from services.fake_http.fake_http import start_fake_http

# ─── Setup Logging ───────────────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/honeypot.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# ─── Configuration ───────────────────────────────────────────────────────────
PORTS = {
    2222: handle_ssh,
    12345: handle_ssh
}
HOST = "0.0.0.0"

# ─── Banner ──────────────────────────────────────────────────────────────────
def show_banner():
    banner = r"""
\033[94m
██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ███╗ ██████╗  █████╗ ████████╗███████╗  
██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║██╔════╝ ██╔══██╗╚══██╔══╝██╔════╝  
██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║██║  ███╗███████║   ██║   █████╗    
██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║██║   ██║██╔══██║   ██║   ██╔══╝    
██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║╚██████╔╝██║  ██║   ██║   ███████╗  
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝  
                                PhantomGate Honeypot Detection System 
\033[0m
\033[94m
[+] PROJECT  : PhantomGate Honeypot Detection System
[+] STATUS   : 🟢 ACTIVE - Monitoring started
[+] PORTS    : 2222 (SSH), 8080 (HTTP), 12345 (Custom Trap), 80 (Redirect)
[+] LOG FILE : logs/honeypot.log
[+] AUTHOR   : Anandhu and Vimal
[+] VERSION  : 1.1
--------------------------------------------------------------------------------
\033[0m
"""
    print(banner)

# ─── Dashboard Auto-Start ─────────────────────────────────────────────────────
def start_dashboard():
    try:
        subprocess.Popen(["python3", "dashboard/app1.py"])
        print("\033[92m[+] Dashboard running at: http://localhost:5000\033[0m")
    except Exception as e:
        print(f"\033[91m[!] Failed to start dashboard: {e}\033[0m")

# ─── Port 80 to 8080 Redirector ──────────────────────────────────────────────
def start_redirector():
    class RedirectHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(302)
            self.send_header('Location', f'http://{self.server.server_address[0]}:8080')
            self.end_headers()

        def log_message(self, format, *args):
            return  # Disable console logging

    try:
        server_address = ('0.0.0.0', 80)
        httpd = HTTPServer(server_address, RedirectHandler)
        print("\033[93m[+] Redirector active: http://<IP> → http://<IP>:8080\033[0m")
        httpd.serve_forever()
    except Exception as e:
        print(f"\033[91m[!] Failed to start port 80 redirector: {e}\033[0m")

# ─── Handle Incoming Connections ─────────────────────────────────────────────
def handle_connection(conn, addr, port):
    ip = addr[0]
    logging.info(f"Connection attempt from {ip}:{port}")
    geoip_info = get_geoip_info(ip)
    if geoip_info:
        logging.info(f"GeoIP Info: {ip} - {geoip_info}")
    handler = PORTS.get(port)
    if handler:
        try:
            handler(conn, ip)
        except Exception as e:
            logging.error(f"Error handling {ip}:{port} - {str(e)}")
    conn.close()

# ─── Listener Thread ─────────────────────────────────────────────────────────
def start_listener(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, port))
    sock.listen(5)
    logging.info(f"Listening on port {port}")
    while True:
        conn, addr = sock.accept()
        threading.Thread(target=handle_connection, args=(conn, addr, port)).start()

# ─── Main ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    show_banner()
    start_dashboard()

    # Start listeners for each service port
    for port in PORTS:
        threading.Thread(target=start_listener, args=(port,), daemon=True).start()

    # Start fake website
    threading.Thread(target=start_fake_http, daemon=True).start()

    # Start HTTP redirector on port 80
    threading.Thread(target=start_redirector, daemon=True).start()

    while True:
        pass  # Keeps main thread running

