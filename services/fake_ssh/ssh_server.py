import socket
import threading
from utils.logger import log_event
from .ssh_filesystem import list_dir, cat_file

def handle_ssh(conn, ip):
    current_path = "/"
    try:
        conn.sendall(b"Welcome to SSH Honeypot!\n")
        conn.sendall(b"login: ")
        username = conn.recv(1024).decode(errors='ignore').strip()

        conn.sendall(b"password: ")
        password = conn.recv(1024).decode(errors='ignore').strip()

        log_event(f"[SSH] Login attempt from {ip} with username: '{username}' and password: '{password}'")

        # Only allow specific credentials
        if username != "vimal" or password != "4442":
            conn.sendall(b"Access denied. Invalid credentials.\n")
            log_event(f"[SSH] Access denied for {ip}")
            return

        conn.sendall(b"Access granted. Type commands:\n")

        while True:
            conn.sendall(f"{current_path}$ ".encode())
            cmd = conn.recv(1024)
            if not cmd:
                break
            cmd_str = cmd.decode(errors='ignore').strip()
            log_event(f"[SSH] {ip} typed command: {cmd_str}")

            if cmd_str.startswith("ls"):
                output = list_dir(current_path)

            elif cmd_str.startswith("cat "):
                try:
                    filepath = cmd_str.split(" ", 1)[1]
                    full_path = filepath if filepath.startswith("/") else current_path.rstrip("/") + "/" + filepath
                    output = cat_file(full_path)
                except IndexError:
                    output = "Usage: cat <filename>"

            elif cmd_str.startswith("cd "):
                try:
                    new_dir = cmd_str.split(" ", 1)[1]
                    if new_dir == "..":
                        current_path = "/".join(current_path.rstrip("/").split("/")[:-1]) or "/"
                    elif new_dir.startswith("/"):
                        current_path = new_dir
                    else:
                        current_path = current_path.rstrip("/") + "/" + new_dir
                    output = ""
                except IndexError:
                    output = "Usage: cd <directory>"

            elif cmd_str == "whoami":
                output = "vimal"

            elif cmd_str == "ps":
                output = (
                    "USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND\n"
                    "root         1  0.0  0.1  22540  3548 ?        Ss   10:00   0:01 /sbin/init\n"
                    "vimal      101  0.1  0.3  55000  7880 pts/0    Ss   10:01   0:03 -bash\n"
                    "vimal      123  0.0  0.2  43210  4216 pts/0    R+   10:02   0:00 ps"
                )

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
            threading.Thread(target=handle_ssh, args=(conn, addr), daemon=True).start()
