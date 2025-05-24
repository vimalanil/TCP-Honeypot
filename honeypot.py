### honeypot.py
import socket
import threading
import logging
import os
from utils.geoip_lookup import get_geoip_info
from services.fake_ssh import handle_ssh
from services.fake_http import handle_http

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/honeypot.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Ports to listen on
PORTS = {
    2222: handle_ssh,  # SSH
    8080: handle_http, # HTTP
    12345: handle_ssh  # Custom or generic fake service
}

HOST = "0.0.0.0"


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


def start_listener(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, port))
    sock.listen(5)
    logging.info(f"Listening on port {port}")

    while True:
        conn, addr = sock.accept()
        threading.Thread(target=handle_connection, args=(conn, addr, port)).start()


if __name__ == "__main__":
    for port in PORTS:
        threading.Thread(target=start_listener, args=(port,), daemon=True).start()

    while True:
        pass  # Keep main thread alive
