import customtkinter as ctk
import socket
import threading

PORT = 12345

# Configurações da interface
ctk.set_appearance_mode("dark") # pode usar o light tbm mas né '-' dark é melhor
ctk.set_default_color_theme("blue")

# Janela principal
app = ctk.CTk()
app.title("Unipinho Chat - Cliente")
app.geometry("400x600")

# Perguntar IP do servidor antes de iniciar
SERVER_IP = ""
while not SERVER_IP:
    dialog = ctk.CTkInputDialog(title="Conectar ao Servidor", text="Digite o IP do servidor (ex: 127.0.0.1):")
    SERVER_IP = dialog.get_input()
    if not SERVER_IP:
        ctk.CTkMessagebox(title="Aviso", message="Você precisa digitar um IP para conectar.", icon="warning")

# Frame principal
frame = ctk.CTkFrame(master=app)
frame.pack(padx=20, pady=20, fill="both", expand=True)

scrollable = ctk.CTkScrollableFrame(master=frame)
scrollable.pack(padx=10, pady=10, fill="both", expand=True)

# Entrada de mensagem
entry_frame = ctk.CTkFrame(master=app)
entry_frame.pack(padx=20, pady=10, fill="x")

entry = ctk.CTkEntry(master=entry_frame, placeholder_text="Digite sua mensagem...")
entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

# Adicionar mensagem ao chat
def add_message(msg, sender="voce"):
    color = "#DCF8C6" if sender == "voce" else "#E5E5EA"
    anchor = "e" if sender == "voce" else "w"
    label = ctk.CTkLabel(
        master=scrollable,
        text=msg,
        fg_color=color,
        text_color="black",
        corner_radius=15,
        justify="left",
        wraplength=250,
        anchor=anchor
    )
    label.pack(anchor=anchor, padx=10, pady=5)

# Enviar mensagem
def send_msg():
    msg = entry.get()
    if msg:
        client.send(msg.encode())
        add_message(f"Você: {msg}", sender="voce")
        entry.delete(0, "end")
        
entry.bind("<Return>", lambda event: send_msg())

send_button = ctk.CTkButton(master=entry_frame, text="Enviar", command=send_msg)
send_button.pack(side="right")

# Receber mensagens
def receive_messages():
    while True:
        try:
            data = client.recv(1024)
            if not data:
                break
            add_message(f"Servidor: {data.decode()}", sender="outro")
        except:
            break

# Conectar ao servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((SERVER_IP, PORT))
except Exception as e:
    ctk.CTkMessagebox(title="Erro", message=f"Erro ao conectar ao servidor:\n{e}", icon="error")
    app.destroy()
    exit()

# Inicia thread de recebimento
threading.Thread(target=receive_messages, daemon=True).start()

# Inicia app
app.mainloop()
