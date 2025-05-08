import socket, threading
from shared.configs import HOST, PORT, BUFFER_SIZE, ENCODING

clients = []
usernames = {}

def broadcast(message, sender=None):
    for client in clients:
        try: client.send(message)
        except: remove_client(client)

def send_private_message(target_username, message):
    for client, name in usernames.items():
        if name == target_username:
            client.send(message.encode(ENCODING))
            return True
    return False

def handle_client(client):
    try:
        client.send("USERNAME".encode(ENCODING))
        username = client.recv(BUFFER_SIZE).decode(ENCODING)
        usernames[client] = username
        clients.append(client)
        broadcast(f"{username} entrou no chat!".encode(ENCODING))

        while True:
            message = client.recv(BUFFER_SIZE).decode(ENCODING)
            if message.startswith("/admin:list"):
                users = "\n".join(usernames.values())
                client.send(f"[SERVER] Online:\n{users}".encode(ENCODING))
            elif message.startswith("/admin:msg "):
                _, target, *msg_parts = message.split()
                msg = " ".join(msg_parts)
                success = send_private_message(target, f"[PRIVADO] [ADMIN]: {msg}")
                if not success:
                    client.send(f"[SERVER] Usuário '{target}' não encontrado.".encode(ENCODING))
            else:
                broadcast(message.encode(ENCODING), client)
    except:
        print(f"Erro ao lidar com o cliente {usernames.get(client, 'Unknown')}: {e}")
        remove_client(client)

def remove_client(client):
    if client in clients: clients.remove(client)
    if client in usernames:
        broadcast(f"{usernames[client]} saiu.".encode(ENCODING))
        del usernames[client]

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Servidor ativo em {HOST}:{PORT}")

    while True:
        client, _ = server.accept()
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()

if __name__ == "__main__":
    main()
