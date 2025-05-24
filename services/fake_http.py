def handle_http(conn, ip):
    try:
        data = conn.recv(1024).decode(errors="ignore")
        if data:
            # Basic HTTP response
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                "Connection: close\r\n\r\n"
                "<html><body><h1>Welcome to Fake HTTP Service</h1></body></html>"
            )
            conn.sendall(response.encode())
    except Exception as e:
        pass  # Silently ignore for now
