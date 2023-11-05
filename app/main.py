import socket

def getPath(data):

    decoded_data = data.decode()
    first_line = decoded_data.split("\r\n")[0]
    path = first_line.split(" ")[1]

    return path

def main():
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    sock, addr = server_socket.accept()  # wait for client
    data = sock.recv(1024)
    path = getPath(data)
    
    if path == "/":
        sock.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    else:
        sock.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

if __name__ == "__main__":
    main()
