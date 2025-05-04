import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
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
            except Exception as e:
                break

    def send(self, message):
        try:
            self.socket.send(message.encode(ENCODING))
        except:
            self.socket.close()
            self.running = False

def send_message():
    msg = message_entry.get()
    user = user_entry.get().strip()
    if not msg:
        return
    if user:
        display_msg = f"[PRIVADO] para {user}: {msg}"
        client.send(f"/admin:msg {user} {msg}")
        on_receive(display_msg)
    else:
        client.send(f"[ADMIN]: {msg}")
    message_entry.set("")

def list_users():
    client.send("/admin:list")

def on_receive(msg):
    if "está digitando..." in msg or "parou de digitar." in msg:
        if not msg.startswith("admin"):
            typing_status_label.config(text=msg if "está digitando" in msg else "")
        return

    if "[PRIVADO]" in msg:
        chat_box.tag_config('private', foreground='#2E7D32', font=('Segoe UI', 10, 'bold'))
        chat_box.config(state=tk.NORMAL)
        chat_box.insert(tk.END, msg + '\n', 'private')
    else:
        chat_box.config(state=tk.NORMAL)
        chat_box.insert(tk.END, msg + '\n')

    chat_box.config(state=tk.DISABLED)
    chat_box.yview(tk.END)

def check_single_instance():
    lock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        lock_socket.bind(('127.0.0.1', 65432))
    except socket.error:
        messagebox.showerror("Erro", "Já existe um painel admin aberto.")
        sys.exit()
    return lock_socket

def configure_styles():
    style = ttk.Style()
    style.theme_use('clam')

    style.configure('.', background='#E8F5E9', foreground='#1B5E20', font=('Segoe UI', 10))

    style.configure('TButton', background='#4CAF50', foreground='white',
                   borderwidth=1, focusthickness=3, focuscolor='#4CAF50',
                   font=('Segoe UI', 10, 'bold'))
    style.map('TButton',
              background=[('active', '#388E3C'), ('pressed', '#2E7D32')],
              foreground=[('active', 'white'), ('pressed', 'white')])


    style.configure('TEntry', fieldbackground='white', borderwidth=1,
                   relief='solid', padding=5)

    style.configure('TLabel', background='#E8F5E9', foreground='#1B5E20')

    style.configure('TFrame', background='#E8F5E9')

lock_socket = check_single_instance()

# === GUI Setup ===
root = tk.Tk()
root.title("Secretaria de Estado do Meio Ambiente - Painel Administrativo")
root.geometry("800x600")
root.configure(bg='#E8F5E9')

configure_styles()

header_frame = ttk.Frame(root, style='TFrame')
header_frame.pack(fill=tk.X, padx=10, pady=10)

ttk.Label(header_frame, text="Painel Administrativo",
          font=('Segoe UI', 16, 'bold'), style='TLabel').pack(side=tk.LEFT)

chat_frame = ttk.Frame(root, style='TFrame')
chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

chat_box = scrolledtext.ScrolledText(
    chat_frame,
    state=tk.DISABLED,
    font=('Segoe UI', 10),
    wrap=tk.WORD,
    bg='white',
    fg='#1B5E20',
    padx=10,
    pady=10,
    insertbackground='#1B5E20',
    selectbackground='#A5D6A7'
)
chat_box.pack(fill=tk.BOTH, expand=True)

typing_status_label = ttk.Label(
    root,
    text="",
    foreground="#689F38",
    font=('Segoe UI', 9, 'italic'),
    style='TLabel'
)
typing_status_label.pack(anchor=tk.W, padx=15)

controls = ttk.Frame(root, style='TFrame')
controls.pack(fill=tk.X, padx=10, pady=(0, 15))

user_controls = ttk.Frame(controls, style='TFrame')
user_controls.pack(side=tk.LEFT)

ttk.Label(user_controls, text="Usuário:", style='TLabel').pack(side=tk.LEFT, padx=(0, 5))

user_entry = tk.StringVar()
user_field = ttk.Entry(
    user_controls,
    textvariable=user_entry,
    width=15,
    style='TEntry'
)
user_field.pack(side=tk.LEFT, ipady=5)

message_entry = tk.StringVar()
entry = ttk.Entry(
    controls,
    textvariable=message_entry,
    width=40,
    style='TEntry'
)
entry.pack(side=tk.LEFT, padx=10, ipady=5, expand=True, fill=tk.X)

button_frame = ttk.Frame(controls, style='TFrame')
button_frame.pack(side=tk.RIGHT)

ttk.Button(button_frame, text="Enviar", command=send_message).pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="Listar Usuários", command=list_users).pack(side=tk.LEFT, padx=5)

footer_frame = ttk.Frame(root, style='TFrame')
footer_frame.pack(fill=tk.X, padx=10, pady=10)
ttk.Label(
    footer_frame,
    text="Secretaria de Estado do Meio Ambiente © 2025",
    style='TLabel',
    font=('Segoe UI', 8)
).pack(side=tk.RIGHT)

client = AdminClient("admin", on_receive)

root.protocol("WM_DELETE_WINDOW", lambda: (client.socket.close(), root.destroy()))

entry.focus()

root.mainloop()