import customtkinter as ctk
import socket
import threading
import tkinter.filedialog as fd

# Configurações do servidor
HOST = '0.0.0.0'
PORT = 12345

# Estilo visual
ctk.set_appearance_mode("dark")  # ou "light"
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Unipinho Chat - Servidor")
app.geometry("400x600")

# Layout principal
frame = ctk.CTkFrame(master=app)
frame.pack(padx=20, pady=20, fill="both", expand=True)

scrollable = ctk.CTkScrollableFrame(master=frame)
scrollable.pack(padx=10, pady=10, fill="both", expand=True)

# Campo de digitação
entry_frame = ctk.CTkFrame(master=app)
entry_frame.pack(padx=20, pady=10, fill="x")

entry = ctk.CTkEntry(master=entry_frame, placeholder_text="Digite sua mensagem...")
entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

# Função para adicionar mensagens com estilo
def add_message(msg, sender="voce"):
    theme = ctk.get_appearance_mode()

    if sender == "voce":
        bg_color = "#DCF8C6" if theme == "light" else "#075E54"
        text_color = "black" if theme == "light" else "white"
        anchor = "e"
    else:
        bg_color = "#E5E5EA" if theme == "light" else "#262D31"
        text_color = "black" if theme == "light" else "white"
        anchor = "w"

    label = ctk.CTkLabel(
        master=scrollable,
        text=msg,
        fg_color=bg_color,
        text_color=text_color,
        corner_radius=15,
        justify="left",
        wraplength=250,
        anchor="w"
    )
    label.pack(anchor=anchor, padx=10, pady=5)

# Envio de mensagens
def send_msg():
    msg = entry.get()
    if msg:
        conn.send(msg.encode())
        add_message(f"Você: {msg}", sender="voce")
        entry.delete(0, "end")

def abrir_janela_emoji():
    emoji_window = ctk.CTkToplevel(app)
    emoji_window.title("Emojis")
    emoji_window.geometry("250x250")

    emojis = ["😁","💻","✅","😎","😍","👨‍🏫","👨‍💻","👩‍💻","❤️"]

    for i, emoji in enumerate(emojis):
        btn = ctk.CTkButton(master=emoji_window, text=emoji, width=40, command=lambda e=emoji: inserir_emoji(e, emoji_window))
        btn.grid(row=i // 5, column=i % 5, padx=5, pady=5)

def inserir_emoji(emoji, window):
    entry.insert("end", emoji)
    window.destroy()

def enviar_arquivo():
    file_path = fd.askopenfilename()
    if file_path:
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            filename = file_path.split("/")[-1]
            header = f"FILE:{filename}".encode()

            conn.send(header)
            conn.send(data)

            add_message(f"Arquivo:{filename}", sender="voce")

        except Exception as e:
            add_message(f"Erro ao enviar arquivo: {e}", sender="voce")

# Adicionando o binding para a tecla Enter
entry.bind("<Return>", lambda event: send_msg())

emoji_button = ctk.CTkButton(master=entry_frame, text="💻", width=30,command=abrir_janela_emoji)
emoji_button.pack(side="left", padx=(0,10))

arquivo_btn = ctk.CTkButton(master=entry_frame, text="📎", width=30, command=enviar_arquivo)
arquivo_btn.pack(side="left", padx=(0,10))

send_button = ctk.CTkButton(master=entry_frame, text="Enviar", command=send_msg)
send_button.pack(side="right")

# Recebimento de mensagens
def receive_messages():
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break

            if data.startswith(b"FILE:"):
                header = data.decode
                _, filename, size = header.split(":")
                size = int(size)
                file_data = b""

                while len(file_data) < size:
                    chunk = conn.recv(1024)
                    if not chunk:
                        break
                    file_data += chunk
                
                with open(filename, "wb") as f:
                    f.write(file_data)

                add_message(f"Cliente enviou um arquivo {filename}", sender="outro")

            else: 
                add_message(f"Cliente: {data.decode()}", sender="outro")
        except Exception as e:
            add_message(f"Erro ao receber: {e}", sender="outro")
            break

# Inicializa servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

add_message("Aguardando conexão...", sender="outro")

conn, addr = server.accept()
add_message(f"Conectado a: {addr}", sender="outro")

# Inicia thread de escuta
threading.Thread(target=receive_messages, daemon=True).start()

app.mainloop() #inicia a janela de conversa
