import socket
import threading
import logging
import os
import subprocess
from utils.geoip_lookup import get_geoip_info
from services.fake_ssh.ssh_server import handle_ssh
from services.fake_http import start_fake_http

# ─── Setup Logging ───────────────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/honeypot.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# ─── Configuration ───────────────────────────────────────────────────────────
PORTS = {
    2222: handle_ssh,         # SSH Trap
    8080: start_fake_http,    # Fake HTTP Server
    12345: handle_ssh         # Custom or generic service
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
[+] PORTS    : 2222 (SSH), 8080 (HTTP), 12345 (Custom Trap)
[+] LOG FILE : logs/honeypot.log
[+] AUTHOR   : Anandhu and Vimal
[+] VERSION  : 1.0
--------------------------------------------------------------------------------
\033[0m
"""
    print(banner)

# ─── Start Dashboard Automatically ───────────────────────────────────────────
def start_dashboard():
    try:
        subprocess.Popen(["python3", "dashboard/app1.py"])
        print("\033[92m[+] Dashboard running at: http://localhost:5000\033[0m")
    except Exception as e:
        print(f"\033[91m[!] Failed to start dashboard: {e}\033[0m")

# ─── Handle Individual Connections ───────────────────────────────────────────
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

# ─── Start Listener on Each Port ─────────────────────────────────────────────
def start_listener(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, port))
    sock.listen(5)
    logging.info(f"Listening on port {port}")

    while True:
        conn, addr = sock.accept()
        threading.Thread(target=handle_connection, args=(conn, addr, port)).start()

# ─── Main Entry ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    show_banner()
    start_dashboard()

    for port in PORTS:
        threading.Thread(target=start_listener, args=(port,), daemon=True).start()

    while True:
        pass  # Keep main thread alive

