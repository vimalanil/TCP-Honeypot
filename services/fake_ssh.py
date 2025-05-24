def handle_ssh(conn, ip):
    try:
        # Send fake SSH banner
        banner = "SSH-2.0-OpenSSH_7.9p1 Debian-10+deb10u2\r\n"
        conn.sendall(banner.encode())

        while True:
            data = conn.recv(1024)
            if not data:
                break
            # Echo back fake response
            response = "Password authentication failed.\r\n"
            conn.sendall(response.encode())
    except Exception as e:
        pass  # Silently ignore for now
