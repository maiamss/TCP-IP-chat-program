import tkinter as tk
from tkinter import ttk, scrolledtext
import socket
import threading
from shared.configs import HOST, PORT, BUFFER_SIZE, ENCODING
import sys

class AdminClient:
    def __init__(self, username, on_receive_callback):
        self.username = username
        self.on_receive_callback = on_receive_callback
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))
        self.running = True
        threading.Thread(target=self.receive, daemon=True).start()

    def receive(self):
        while self.running:
            try:
                msg = self.socket.recv(BUFFER_SIZE).decode(ENCODING)
                if msg == "USERNAME":
                    self.socket.send(self.username.encode(ENCODING))
                else:
                    self.on_receive_callback(msg)
            except:
                break

    def send(self, message):
        try:
            self.socket.send(message.encode(ENCODING))
        except:
            self.socket.close()
            self.running = False

# === GUI Logic ===
def send_message():
    msg = message_entry.get()
    user = user_entry.get().strip()
    if not msg:
        return
    if user:
        client.send(f"/admin:msg {user} {msg}")
    else:
        client.send(f"[ADMIN]: {msg}")
    message_entry.set("")

def list_users():
    client.send("/admin:list")

def on_receive(msg):
    if msg.endswith("is typing...") or msg.endswith("stopped typing."):
        typing_status_label.config(text=msg if "is typing" in msg else "")
        return
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, msg + '\n')
    chat_box.config(state=tk.DISABLED)
    chat_box.yview(tk.END)

def check_single_instance():
    lock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        lock_socket.bind(('127.0.0.1', 65432))  # Porta exclusiva para o painel
    except socket.error:
        print("Já existe um painel admin aberto.")
        sys.exit()
    return lock_socket

# Impede múltiplas instâncias
lock_socket = check_single_instance()

# === GUI Setup ===
root = tk.Tk()
root.title("Secretaria de Estado do Meio Ambiente - Painel Admin")
root.geometry("750x500")

chat_box = scrolledtext.ScrolledText(root, state=tk.DISABLED, font=("Segoe UI", 10))
chat_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

controls = ttk.Frame(root)
controls.pack(fill=tk.X, padx=10)

message_entry = tk.StringVar()
entry = ttk.Entry(controls, textvariable=message_entry, width=40)
entry.pack(side=tk.LEFT, padx=5)

user_entry = tk.StringVar()
user_field = ttk.Entry(controls, textvariable=user_entry, width=15)
user_field.pack(side=tk.LEFT, padx=5)

ttk.Button(controls, text="Enviar", command=send_message).pack(side=tk.LEFT, padx=5)
ttk.Button(controls, text="Listar Usuários", command=list_users).pack(side=tk.LEFT, padx=5)

client = AdminClient("admin", on_receive)

root.protocol("WM_DELETE_WINDOW", lambda: (client.socket.close(), root.destroy()))
root.mainloop()
