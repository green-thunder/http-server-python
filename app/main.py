import socket
import threading

def getPath(data):

    decoded_data = data.decode()
    first_line = decoded_data.split("\r\n")[0]
    path = first_line.split(" ")[1]

    return path

def getHeaderUserAgent(data):

    decoded_data = data.decode()
    first_line = decoded_data.split("\r\n")

    for header in first_line:
        if header.startswith("User-Agent:"):
            return header.split(" ")[1]

def handle_request(sock: socket.socket):

    data = sock.recv(1024)
    path = getPath(data)
    
    if path == "/":
        sock.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

    elif path.startswith("/echo/"):
        
        message = path.split("/echo/")[1]
        sock.send(b"HTTP/1.1 200 OK\r\n")
        sock.send(b"Content-Type: text/plain\r\n")
        length = f"Content-Length: {len(message)} \r\n"
        sock.send(length.encode())
        sock.send(b"\r\n")
        sock.send(message.encode())

    elif path == "/user-agent":

        message = getHeaderUserAgent(data)
        sock.send(b"HTTP/1.1 200 OK\r\n")
        sock.send(b"Content-Type: text/plain\r\n")
        length = f"Content-Length: {len(message)} \r\n"
        sock.send(length.encode())
        sock.send(b"\r\n")
        sock.send(message.encode())

    else:
        sock.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
    sock.close()

def main():
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        sock, addr = server_socket.accept()  # wait for client
        thread = threading.Thread(target=handle_request, args=(sock,)).start()


if __name__ == "__main__":
    main()
