#thread para cada cliente conectado
def connect_client(new_socket, address):
    print(f"NEW CONNECTION -> Connected client: {address}.")
    while True:
        data = new_socket.recv(1024) #loop criado para receber todos os dados que o cliente enviar (1024: tamanho máximo, em bytes, que o server vai ler de uma vez)
        if not data:
            break #se nenhum dado estiver sendo lido, o server é fechado
        new_socket.sendall(data) #sendall tentár enviar tudo até o final
    print("Connection closed.")