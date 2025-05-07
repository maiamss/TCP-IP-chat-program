from shared.configs import PORT, BUFFER_SIZE, ENCODING
import socket
import threading

class ChatClient:
    def __init__(self, username, host, port, on_message_callback):
        self.username = username
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.on_message_callback = on_message_callback
        self.running = True
        threading.Thread(target=self.receive, daemon=True).start()

    def receive(self):
        while self.running:
            try:
                message = self.socket.recv(BUFFER_SIZE).decode(ENCODING)
                if message == "USERNAME":
                    self.socket.send(self.username.encode(ENCODING))
                else:
                    self.on_message_callback(message)
            except:
                break

    def send(self, message):
        try:
            self.socket.send(message.encode(ENCODING))
        except:
            self.close()

    def close(self):
        self.running = False
        try:
            self.socket.close()
        except:
            pass
