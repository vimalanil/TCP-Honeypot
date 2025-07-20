# services/fake_ssh.py

import socket
import threading
from utils.logger import log_event
from services.fake_ssh.ssh_filesystem import list_dir, cat_file

def handle_ssh(conn, ip):
    current_path = "/home/vimal"
    try:
        conn.sendall(b"Welcome \n")
        conn.sendall(b"login: ")
        username = conn.recv(1024).decode(errors='ignore').strip()

        conn.sendall(b"password: ")
        password = conn.recv(1024).decode(errors='ignore').strip()

        log_event(f"[SSH] Login attempt from {ip} with username: '{username}' and password: '{password}'")

        if username != "vimal" or password != "4442":
            conn.sendall(b"Access denied. Invalid credentials.\n")
            log_event(f"[SSH] Access denied for {ip}")
            return

        conn.sendall(b"Access granted. Type commands:\n")

        while True:
            conn.sendall(f"[{username}@prsec63 {current_path}]$ ".encode())
            cmd = conn.recv(1024)
            if not cmd:
                break
            cmd_str = cmd.decode(errors='ignore').strip()
            log_event(f"[SSH] {ip} typed command: {cmd_str}")

            if cmd_str == "ls":
                output = list_dir(current_path)

            elif cmd_str == "pwd":
                output = current_path

            elif cmd_str.startswith("cd "):
                new_dir = cmd_str[3:].strip()
                if new_dir == "..":
                    current_path = "/".join(current_path.rstrip("/").split("/")[:-1]) or "/"
                    output = ""
                elif new_dir.startswith("/"):
                    current_path = new_dir
                    output = ""
                else:
                    current_path = current_path.rstrip("/") + "/" + new_dir
                    output = ""
                    
            elif cmd_str.startswith("cat "):
                filepath = cmd_str.split(" ", 1)[1]
                full_path = filepath if filepath.startswith("/") else current_path.rstrip("/") + "/" + filepath
                output = cat_file(full_path)

            elif cmd_str.startswith("nano "):
                filename = cmd_str.split(" ", 1)[1]
                full_path = filename if filename.startswith("/") else current_path.rstrip("/") + "/" + filename
                output = f"Simulated nano editor for {full_path}.\n(Editing not allowed in honeypot)"

            elif cmd_str == "clear":
                output = "\033c"  # ANSI escape to clear screen

            elif cmd_str == "whoami":
                output = "vimal"

            elif cmd_str == "exit":
                conn.sendall(b"Logout successful.\n")
                break

            else:
                output = f"bash: {cmd_str}: command not found"

            conn.sendall((output + "\n").encode())

    except Exception as e:
        log_event(f"[SSH] Error with client {ip}: {e}")
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
            threading.Thread(target=handle_ssh, args=(conn, addr[0]), daemon=True).start()

