#ponto de entrada do servidor
import socket

def initialize_server():
    #definição de host e porta TCP
    host = "127.0.0.1"
    port = 5050

    #criação do socket tcp
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: #constantes: fámilia de endereços e o tipo de socket
        server_socket.bind((host, port)) #ligação do socket criado ao host e port
        server_socket.listen() #socket no modo escuta
        new_socket, adress = server_socket.accept() #socket novo para comunicação com o cliente/endereço do cliente (tupla com host e port)

        with new_socket: 
            print(f"NEW CONNECTION -> Connected client: {adress}") 
            while True:
                data = new_socket.recv(1024) #loop criado para receber todos os dados que o cliente enviar (1024: tamanho máximo, em bytes, que o server vai ler de uma vez)
                if not data:
                    break #se nenhum dado estiver sendo lido, o server é fechado
                new_socket.sendall(data) #sendall tentár enviar tudo até o final

if __name__ == "__main__": #proteção ao código
    initialize_server()