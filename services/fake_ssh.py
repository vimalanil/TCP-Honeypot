import socket
import threading
from utils.logger import log_event

def handle_ssh(conn, addr):
    try:
        conn.sendall(b"Welcome to SSH Honeypot!\n")
        conn.sendall(b"login: ")
        username = conn.recv(1024).decode(errors='ignore').strip()

        conn.sendall(b"password: ")
        password = conn.recv(1024).decode(errors='ignore').strip()

        log_event(f"[SSH] Login attempt from {addr[0]} with username: '{username}' and password: '{password}'")

        conn.sendall(b"Access granted. Type commands:\n")

        while True:
            conn.sendall(b"$ ")
            cmd = conn.recv(1024)
            if not cmd:
                break
            cmd_str = cmd.decode(errors='ignore').strip()
            log_event(f"[SSH] {addr[0]} typed command: {cmd_str}")

            # Respond with a fake command-not-found message
            conn.sendall(b"Command not found\n")

    except Exception as e:
        log_event(f"[SSH] Error with client {addr[0]}: {e}")
    finally:
        conn.close()

def start_fake_ssh(host='0.0.0.0', port=2222):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(5)
        log_event(f"Fake SSH server listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
