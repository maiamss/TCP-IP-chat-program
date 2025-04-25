#ponto de entrada do servidor
import socket
import threading
from server.client_thread import connect_client

def initialize_server():
    #definição de host e porta TCP
    host = "127.0.0.1"
    port = 5050

    #criação do socket tcp
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: #constantes: fámilia de endereços e o tipo de socket
        server_socket.bind((host, port)) #ligação do socket criado ao host e port
        server_socket.listen() #socket no modo escuta

        #aceita uma nova conexão
        with True: 
            new_socket, address = server_socket.accept() #socket novo para comunicação com o cliente/endereço do cliente (tupla com host e port)
            client_handler = threading.Thread(target=connect_client, args=(new_socket, address)) #cria uma nova thread, função que será executada na thred e seus argumentos
            client_handler.start() #inicialização da thread
