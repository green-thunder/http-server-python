import argparse
from pathlib import Path
import socket
import sys
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

def getFileContent(directory_path, file_path):

    whole_path = Path(directory_path).joinpath(Path(file_path))
    
    if whole_path.exists():
        print("exists")
        
        with open(whole_path, "r") as file:
            file_contents = file.read()
        return True, file_contents
    
    return False, ""


def handle_request(sock: socket.socket, directory_path: str):

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
    elif path.startswith("/files/"):

        file_path = path.split("/files/")[1]
        print(file_path)
        file_exists, content = getFileContent(directory_path, file_path)
        print(content)
        if file_exists:
            sock.send(b"HTTP/1.1 200 OK\r\n")
            sock.send(b"Content-Type: application/octet-stream\r\n")
            length = f"Content-Length: {len(content)} \r\n"
            sock.send(length.encode())
            sock.send(b"\r\n")
            sock.send(content.encode())
        else:
            sock.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

    else:
        sock.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
    sock.close()

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", help="the directory path")
    args = parser.parse_args()
    directory_path = args.directory or None
    print(directory_path)

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        sock, addr = server_socket.accept()  # wait for client
        thread = threading.Thread(target=handle_request, args=(sock, directory_path)).start()


if __name__ == "__main__":
    main()
