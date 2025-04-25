import socket

def initialize_server():

    host = "127.0.0.1"
    port = 5050

    #criação do socket tcp
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: 
        server_socket.bind((host, port)) 
        server_socket.listen() 
        new_socket, adress = server_socket.accept() 

        with new_socket: 
            print(f"NEW CONNECTION -> Connected client: {adress}") 
            while True:
                data = new_socket.recv(1024) 
                if not data:
                    break 
                new_socket.sendall(data) 

if __name__ == "__main__":
    initialize_server()