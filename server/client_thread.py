def connect_client(new_socket, address):
    print(f"NEW CONNECTION -> Connected client: {address}.")
    while True:
        data = new_socket.recv(1024) 
        if not data:
            break 
        new_socket.sendall(data) 
    print("Connection closed.")