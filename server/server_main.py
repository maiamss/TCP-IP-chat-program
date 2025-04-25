import socket
import threading
from server.client_thread import connect_client

def initialize_server():
    host = "127.0.0.1"
    port = 5050

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: 
        server_socket.bind((host, port)) 
        server_socket.listen() 

        with True: 
            new_socket, address = server_socket.accept() 
            client_handler = threading.Thread(target=connect_client, args=(new_socket, address)) 
            client_handler.start() 
